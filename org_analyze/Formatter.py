from typing import List

class Formatter:
    def link(self, url: str, name: str) -> str:
        raise NotImplementedError
    def bold(self, text: str) -> str:
        raise NotImplementedError
    def inline_code(self, text: str) -> str:
        raise NotImplementedError
    def header(self, text: str, level: int) -> str:
        raise NotImplementedError
    def list(self, items: List[str], ordered: bool = False) -> str:
        raise NotImplementedError
    def code(self, items: List[str], language: str) -> str:
        raise NotImplementedError

class MarkdownFormatter(Formatter):
    def link(self, url: str, name: str) -> str:
        if name is None:
            return f"[[{url}]]"
        return f"[{name}]({url})"

    def bold(self, text: str) -> str:
        return f"**{text}**"

    def inline_code(self, text: str) -> str:
        return f"`{text}`"

    def header(self, text: str, level: int) -> str:
        return f"{'#' * level} {text}"

    def list(self, items: List[str], ordered: bool = False) -> str:
        result = []
        for idx, line in enumerate(items):
            prefix = f"{idx + 1}. " if ordered else "- "
            result.append(f"{prefix}{line}")
        return "\n".join(result)

    def code(self, items: List[str], language: str) -> str:
        result = [f"```{language}"]
        result.extend(items)
        result.append("```")
        return "\n".join(result)
        

class HtmlFormatter(Formatter):
    def link(self, url: str, name: str) -> str:
        if name is None:
            return f"<a href=\"{url}\">{url}</a>"
        return f"<a href=\"{url}\">{name}</a>"

    def bold(self, text: str) -> str:
        return f"<strong>{text}</strong>"

    def inline_code(self, text: str) -> str:
        return f"<code>{text}</code>"

    def header(self, text: str, level: int) -> str:
        return f"<h{level}>{text}</h{level}>"

    def list(self, items: List[str], ordered: bool = False) -> str:
        result = ["<ul>"]
        for line in items:
            result.append(f"<li>{line}</li>")
        result.append("</ul>")
        return "\n".join(result)

    def code(self, items: List[str], language: str) -> str:
        if language == "math":
            result = ['\[']
            result.extend(items)
            result.append('\]')
            return "\n".join(result)
        result = [f'<pre><code class="language-{language}">']
        result.extend(items)
        result.append("</code></pre>")
        return "\n".join(result)
