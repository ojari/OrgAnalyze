import os
from org_analyze.org2html import export_html

class DummyNode:
    def __init__(self, file:str):
        self.id = file.replace(".org", "")
        self.title = self.id
        self.file = file


class DummmyRoamDB:
    def __init__(self, org_path: str):
        self.files = os.listdir(org_path)
        self.nodes = [DummyNode(f) for f in self.files]
    
    def get_links(self, orgfile: str):
        return self.nodes

    def filename2node(self, filename: str):
        return next((node for node in self.nodes if node.file == filename), None)

class HtmlConverter:
    def __init__(self, dest_path: str, roam: DummmyRoamDB):
        self.dest_path = dest_path
        self.roam = roam

    def link_converter(self, link: str, name: str) -> str:
        print(f"Converting link: {link} with name: {name}")
        if link.startswith("file:"):
            _, hash = link.split(":", 1)
            return hash.replace(".org", ".html"), name
        return link, name

    def handle_file(self, org_file: str, md_file: str) -> None:
        formatter = HtmlConverter()
        print(f"Processing file: {org_file} -> {md_file}")
        with open(md_file, "w", encoding="utf-8") as md_file_obj:
            for line in export_html(org_file, self.link_converter, self.roam, formatter=formatter):
                if isinstance(line, list):
                    md_file_obj.write("\n".join(line))
                    md_file_obj.write("\n")
                else:
                    md_file_obj.write(line+"\n")

def main():
    org_path = "org/"
    roam_db = DummmyRoamDB(org_path)
    converter = HtmlConverter(org_path, roam_db)
    for file in roam_db.files:
        print(":::"+file)
        html_filename = "docs/" + file.replace(".org", ".html")
        converter.handle_file(org_path + file, html_filename)


if __name__ == "__main__":
    main()
