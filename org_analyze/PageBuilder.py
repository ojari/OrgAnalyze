from typing import List, Sequence, Tuple, Union, Optional

class PageBuilder:
    def add_main_content(self, html: List[str]):
        raise NotImplementedError
    def add_side_link(self, html: List[str]):
        raise NotImplementedError
    def render(self) -> List[str]:
        raise NotImplementedError

class MarkdownPageBuilder(PageBuilder):
    def __init__(self):
        self.main_content: List[str] = []
        self.side_links: List[str] = []
    def add_main_content(self, html: List[str]):
        self.main_content.append(html)
    def add_side_link(self, html: List[str]):
        self.side_links.append(html)
    def render(self) -> List[str]:
        page = []
        page.extend(self.main_content)
        page.append("\n## Links\n")
        page.extend(self.side_links)
        return page


class HtmlPageBuilder(PageBuilder):
    def __init__(self, title: str):
        self.title = title
        self.header = self._build_header()
        self.footer = self._build_footer()
        self.main_content: List[str] = []
        self.side_links: List[str] = []

    def _build_header(self) -> List[str]:
        return [
            "<!DOCTYPE html>",
            "<html>",
            "<head>",
            f"<meta charset=\"utf-8\">",
            f"<title>{self.title}</title>",
            '<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>',
            "<style>",
            "body { background: #3F3F3F; color: #DCDCCC; font-family: 'Segoe UI', 'Arial', sans-serif; }",
            ".container { display: flex; flex-direction: row; }",
            ".main-content { flex: 3; padding: 16px; }",
            ".side-links { flex: 1; padding: 16px; background: #2B2B2B; color: #93E0E3; min-width: 200px; }",
            "h1, h2, h3, h4, h5, h6 { color: #F0DFAF; }",
            "table { background: #4F4F4F; color: #DCDCCC; border-collapse: collapse; }",
            "th, td { border: 1px solid #6F6F6F; padding: 4px 8px; }",
            "th { background: #5F5F5F; color: #F0DFAF; }",
            "pre, code { background: #2B2B2B; color: #CC9393; font-family: 'Fira Mono', 'Consolas', 'Monaco', monospace; }",
            ".math { background: #2B2B2B; color: #DFAF8F; padding: 8px; display: block; }",
            "a { color: #93E0E3; }",
            "</style>",
            "</head>",
            "<body>",
            '<div class="container">'
        ]

    def _build_footer(self) -> List[str]:
        return [
            "</div>",  # end container
           "</body>",
            "</html>"
        ]

    def add_main_content(self, html: List[str]):
        self.main_content.append(html)

    def add_side_link(self, html: List[str]):
        self.side_links.append(html)

    def render(self) -> List[str]:
        page = []
        page.extend(self.header)
        page.append('<div class="main-content">')
        page.extend(self.main_content)
        page.append('</div>')
        page.append('<div class="side-links">')
        page.append('<h2>Links</h2>')
        page.extend(self.side_links)
        page.append('</div>')
        page.extend(self.footer)
        return page
