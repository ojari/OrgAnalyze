import os
import tempfile
import pytest
from org_analyze.ParserOrg import (
    ParserOrg,
    OrgHeader,
    OrgTable,
    OrgText,
    OrgList,
    OrgProperties,
    OrgSourceBlock,
    OrgMath,
    OrgClock
)

class OrgFileHelper:
    """Context manager that writes an org snippet to a temp file, parses it, and cleans up."""
    def __init__(self, content: str):
        self.content = content
        self.path = None
        self.items = None

    def link_converter(self, link: str, name: str) -> str:
        return f"url({link})", f"name({name})"

    def __enter__(self):
        tmp = tempfile.NamedTemporaryFile("w+", delete=False, suffix=".org", encoding="utf-8")
        tmp.write(self.content)
        tmp.flush()
        tmp.close()
        self.path = tmp.name
        with ParserOrg(self.path, self.link_converter) as parser:
            self.items = parser.parse()
        return self

    def __exit__(self, exc_type, exc, tb):
        if self.path and os.path.exists(self.path):
            os.remove(self.path)


def test_headers_and_text():
    content = """* Heading 1
Some text.
** Subheading
More text.

"""
    with OrgFileHelper(content) as org:
        assert any(isinstance(i, OrgHeader) and i.name == "Heading 1" for i in org.items)
        assert any(isinstance(i, OrgHeader) and i.name == "Subheading" for i in org.items)
        assert any(isinstance(i, OrgText)   and ("Some text." in i.line) for i in org.items)
        assert any(isinstance(i, OrgText)   and ("More text." in i.line) for i in org.items)


def test_table_parsing():
    content = """* Table Example
| Name | Value |
|------|-------|
| Foo  | 123   |
| Bar  | 456   |
"""
    with OrgFileHelper(content) as org:
        tables = [i for i in org.items if isinstance(i, OrgTable)]
        assert len(tables) == 1
        table = tables[0]
        assert table.rows[0] == ["Name", "Value"]
        assert table.rows[1] == ["Foo", "123"]
        assert table.rows[2] == ["Bar", "456"]


def test_list_and_properties():
    content = """* List Example
:PROPERTIES:
:Custom: Value
:END:

- item 1
- item 2
"""
    with OrgFileHelper(content) as org:
        assert any(isinstance(i, OrgProperties) and i.values.get("custom") == "Value" for i in org.items)
        lists = [i for i in org.items if isinstance(i, OrgList)]
        assert len(lists) == 1
        assert lists[0].lines[0] == "item 1"
        assert lists[0].lines[1] == "item 2"

def test_source_block_and_math():
    content = """* Source and Math
#+BEGIN_SRC python
print("Hello")
#+END_SRC
\\[
x^2 + y^2 = z^2
\\]
"""
    with OrgFileHelper(content) as org:
        assert any(isinstance(i, OrgSourceBlock) and "print(\"Hello\")" in i.lines for i in org.items)
        assert any(isinstance(i, OrgMath) and "x^2 + y^2 = z^2" in i.lines for i in org.items)

        
def test_clock():
    content = """* Clockins
CLOCK: [2025-06-01 Sat 10:00]--[2025-06-01 Sat 11:00] =>  1:00
"""
    with OrgFileHelper(content) as org:
        clock = [i for i in org.items if isinstance(i, OrgClock)]
        assert len(clock) == 1
        assert clock[0].start == "2025-06-01"
        assert clock[0].duration == "1:00"

                
def test_clock_2():
    content = """* Clockins
#+CLK: [2025-07-02 Sat 4:00]
"""
    with OrgFileHelper(content) as org:
        clock = [i for i in org.items if isinstance(i, OrgClock)]
        assert len(clock) == 1
        assert clock[0].start == "2025-07-02"
        assert clock[0].duration == "4:00"

        
def test_link():
    content = """ [[http://example.com][Example Link]]
"""
    with OrgFileHelper(content) as org:
        text = [i for i in org.items if isinstance(i, OrgText)]
        assert text[0].line == " [name(Example Link)](url(http://example.com))"

def test_link_header():
    content = """** [[http://example.com][Example Link]]
"""
    with OrgFileHelper(content) as org:
        headers = [i for i in org.items if isinstance(i, OrgHeader)]
        assert headers[0].level == 2
        assert headers[0].name == "[name(Example Link)](url(http://example.com))"

def test_link_list():
    content = """* List with link
- [[http://example.com][Example Link]]
- another
"""
    with OrgFileHelper(content) as org:
        lst = [i for i in org.items if isinstance(i, OrgList)]
        assert lst[0].lines[0] == "[name(Example Link)](url(http://example.com))"
        assert lst[0].lines[1] == "another"
