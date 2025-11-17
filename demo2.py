# Converts Org-roam database to Markdown files.
#
# from org_analyze import export_markdown as export
from org_analyze import export_html as export
from org_analyze.RoamDb import RoamDB
import os
from typing import List, Self

#EXTENSION = ".md"
EXTENSION = ".html"

class MarkdownConverter:
    def __init__(self, roam: RoamDB, dest_path: str):
        self.roam = roam
        self.dest_path = dest_path

    def link_converter(self, link: str, name: str) -> str:
        if link.startswith("id:"):
            _, hash = link.split(":", 1)
            roam_node = self.roam.id2node(hash)
            if roam_node is not None:
                fname = self.dest_path + roam_node.file.replace(".org", EXTENSION)
                return fname, name
            return name, None
        return link, name

    def handle_file(self, org_file: str, md_file: str) -> None:
        print(f"Processing file: {org_file} -> {md_file}")
        with open(md_file, "w", encoding="utf-8") as md_file_obj:
            for line in export(org_file, self.link_converter, self.roam, self.dest_path):
                md_file_obj.write(line + "\n")


def create_folders(files: List[str]):
    folders = set([file.split("/")[0] for file in files if ("/" in file)])
    os.makedirs("tmp", exist_ok=True)
    for folder in folders:
        print(f"Creating folder tmp/{folder}...")
        os.makedirs(os.path.join("tmp", folder.lstrip("/")), exist_ok=True)
    return folders


def main():
    org_path = "c:/home/jari/org-roam/"
    out_path = "c:/home/jari/OrgAnalyze/tmp/"
    db_file = os.path.join("..", ".emacs.d", "org-roam.db")
    roam_db = RoamDB(org_path)
    roam_db.load(db_file)

    create_folders(roam_db.get_files())
    converter = MarkdownConverter(roam_db, out_path)

    for file in roam_db.files:
        md_filename = os.path.join("tmp", file.replace(".org", EXTENSION))
        converter.handle_file(org_path + file, md_filename)


if __name__ == "__main__":
    main()
