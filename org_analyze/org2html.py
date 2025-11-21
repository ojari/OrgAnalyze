from re import I
from .ParserOrg import ParserOrg, OrgHeader, OrgClock, OrgTable, OrgSourceBlock, OrgText, OrgMath, OrgProperties, OrgList
from .Formatter import HtmlFormatter
from .PageBuilder import PageBuilder, HtmlPageBuilder
from typing import List, Sequence, Tuple, Union, Optional

def link_converter(link: str, name: str) -> str:
    if link.startswith("id:"):
        return f"<a href=\"{name}.html\">{name}</a>"
    return f"<a href=\"{link}\">{name}</a>"


def export_html(orgfile: str, lnconv=None, roam=None, dest_path="", formatter=None, builder=None) -> List[str]:
    builder : PageBuilder = builder or HtmlPageBuilder("Org Export")
    if lnconv is None:
        lnconv = link_converter
    formatter = formatter or HtmlFormatter()
    with ParserOrg(orgfile, lnconv, formatter) as p:
        result : List[str] = []
        for item in p.parse():
            if isinstance(item, OrgHeader):
                result.append(formatter.header(item.name, item.level))
            elif isinstance(item, OrgProperties):
                print(item.values)
            elif isinstance(item, OrgClock):
                pass # do nothing for now
            elif isinstance(item, OrgTable):
                result.append("<table>")
                if item.rows:
                    # Table header
                    result.append("<tr>" + "".join(f"<th>{cell}</th>" for cell in item.rows[0]) + "</tr>")
                    # Table rows
                    for row in item.rows[1:]:
                        result.append("<tr>" + "".join(f"<td>{cell}</td>" for cell in row) + "</tr>")
                result.append("</table>")
            elif isinstance(item, OrgSourceBlock):
                result.append(formatter.code(item.lines, item.language))
            elif isinstance(item, OrgText):
                result.append(formatter.text_line(item.line))
            elif isinstance(item, OrgMath):
                result.append(formatter.code(item.lines, 'math'))
            elif isinstance(item, OrgList):
                result.append(formatter.list(item.lines))
        builder.add_main_content(result)

        links = []
        if roam is not None:
            for node in roam.get_links(orgfile):
                url = dest_path + node.file.replace(".org", ".html")
                links.append(formatter.text_line(formatter.link(url, node.title)))
        builder.side_links.extend(links)

    return builder.render()
