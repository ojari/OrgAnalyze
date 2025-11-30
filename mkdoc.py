import os
from org_analyze.org2html import export_html


class HtmlConverter:
    def __init__(self, dest_path: str):
        self.dest_path = dest_path

    def link_converter(self, link: str, name: str) -> str:
        print(f"Converting link: {link} with name: {name}")
        if link.startswith("file:"):
            _, hash = link.split(":", 1)
            return hash.replace(".org", ".html"), name
        return link, name

    def handle_file(self, org_file: str, md_file: str) -> None:
        print(f"Processing file: {org_file} -> {md_file}")
        with open(md_file, "w", encoding="utf-8") as md_file_obj:
            for line in export_html(org_file, self.link_converter, None, self.dest_path):
                if isinstance(line, list):
                    md_file_obj.write("\n".join(line))
                    md_file_obj.write("\n")
                else:
                    md_file_obj.write(line+"\n")

def main():
    org_path = "org/"
    converter = HtmlConverter(org_path)
    for file in os.listdir("org"):
        print(file)
        html_filename = "docs/" + file.replace(".org", ".html")
        converter.handle_file(org_path + file, html_filename)


if __name__ == "__main__":
    main()
