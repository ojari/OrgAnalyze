# Converts Org-roam database to Markdown files.
#
from org_analyze import export_markdown
import os
import sqlite3
from typing import List

class Node:
    def __init__(self, id: str, title: str, file: str):
        self.id = id[1:-1]
        self.title = title
        self.file = file

    def base_name(self) -> str:
        return os.path.splitext(os.path.basename(self.file))[0]

    def __str__(self):
        return f"Node(id='{self.id}', title='{self.title}', file='{self.file}')"


class OrgRoamDB:
    def __init__(self):
        self.nodes: List[Node] = []
        self.files: List[str] = []

    def load(self, db_path: str):
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, title, file FROM nodes;")
            rows = cursor.fetchall()
            self.nodes = [Node(row[0], row[1], row[2]) for row in rows]

            cursor.execute("SELECT file FROM files;")
            rows = cursor.fetchall()
            self.files = [self.convert_filename(row[0]) for row in rows]

    @staticmethod
    def convert_filename(filename: str) -> str:
        prefix = '"c:/home/jari/org-roam/'
        if filename.startswith(prefix):
            return filename[len(prefix):-1]
        return filename


class MarkdownConverter:
    def __init__(self, nodes: List[Node]):
        self.nodes = nodes

    def md_link_converter(self, link: str, name: str) -> str:
        if link.startswith("id:"):
            hash = link[3:]
            roam_node = next((node for node in self.nodes if node.id == hash), None)
            if roam_node is not None:
                return f"[[{roam_node.base_name()}]]"
            return f"[[{name}]]"
        return f"[{name}]({link})"

    def handle_file(self, org_file: str, md_file: str) -> None:
        print(f"Processing file: {org_file} -> {md_file}")
        with open(md_file, "w", encoding="utf-8") as md_file_obj:
            for line in export_markdown(org_file, self.md_link_converter):
                md_file_obj.write(line + "\n")

    def handle_folder(self, source_base: str, folder: str) -> None:
        for file in os.listdir(os.path.join(source_base, folder)):
            if file.endswith(".org"):
                print(f"{file}...")
                md_filename = os.path.splitext(file)[0] + ".md"
                self.handle_file(
                    os.path.join(source_base, folder, file),
                    os.path.join("tmp", folder, md_filename))


def create_folders(files: List[str]):
    folders = set([file.split("/")[0] for file in files if ("/" in file)])
    os.makedirs("tmp", exist_ok=True)
    for folder in folders:
        print(f"Creating folder tmp/{folder}...")
        os.makedirs(os.path.join("tmp", folder.lstrip("/")), exist_ok=True)
    return folders


def main():
    db_path = os.path.join("..", ".emacs.d", "org-roam.db")
    roam_db = OrgRoamDB()
    roam_db.load(db_path)

    create_folders(roam_db.files)
    converter = MarkdownConverter(roam_db.nodes)

    for file in roam_db.files:
        md_filename = os.path.join("tmp", file.replace(".org", ".md"))
        org_filename = os.path.join("..", "org-roam", file)
        print(f"Processing file: {org_filename} -> {md_filename}...")
        converter.handle_file(org_filename, md_filename)


if __name__ == "__main__":
    main()
