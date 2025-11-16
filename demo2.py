# Converts Org-roam database to Markdown files.
#
# from org_analyze import export_markdown as export
from org_analyze import export_html as export
import os
import sqlite3
from typing import List

#EXTENSION = ".md"
EXTENSION = ".html"

class Node:
    def __init__(self, id: str, title: str, file: str):
        self.id = id[1:-1]
        self.title = title
        if file.startswith("\""):
            self.file = file[1:-1]
        else:
            self.file = file

    def base_name(self) -> str:
        return os.path.splitext(os.path.basename(self.file))[0]

    def __str__(self):
        return f"Node(id='{self.id}', title='{self.title}', file='{self.file}')"

def unquote(s: str) -> str:
    if s.startswith("\"") and s.endswith("\""):
        return s[1:-1]
    return s

class Link:
    def __init__(self, source: str, destination: str, type: str):
        self.source = unquote(source)
        self.destination = unquote(destination)
        self.type = type

class OrgRoamDB:
    def __init__(self):
        self.nodes: List[Node] = []
        self.files: List[str] = []
        self.links: List[Link] = []

    def load(self, db_path: str):
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, title, file FROM nodes;")
            rows = cursor.fetchall()
            self.nodes = [Node(row[0], row[1], row[2]) for row in rows]

            cursor.execute("SELECT file FROM files;")
            rows = cursor.fetchall()
            self.files = [self.convert_filename(row[0]) for row in rows]

            cursor.execute("SELECT source, dest, type FROM links;")
            rows = cursor.fetchall()
            self.links = [Link(row[0], row[1], row[2]) for row in rows]

    def filename2id(self, filename: str):
        return next(
            (node.id for node in self.nodes if node.file == filename or self.convert_filename(node.file) == filename),
            None
        )

    def id2node(self, node_id: str) -> Node:
        return next((node for node in self.nodes if node.id == node_id), None)

    def get_links(self, filename: str):
        node_id = self.filename2id(filename)
        if node_id is None:
            return []
        a = [self.id2node(link.destination) for link in self.links if link.source == node_id]
        b = [self.id2node(link.source) for link in self.links if link.destination == node_id]

        a.extend(b)
        return [node for node in a if node is not None]
        #return [self.id2node(link) for link in self.links if link.source == node_id or link.destination == node_id]  

    @staticmethod
    def convert_filename(filename: str) -> str:
        prefix = '"c:/home/jari/org-roam/'
        if filename.startswith(prefix):
            return filename[len(prefix):-1]
        return filename


class MarkdownConverter:
    def __init__(self, roam: OrgRoamDB):
        self.roam = roam

    @staticmethod
    def link(link: str, name: str) -> str:
        if EXTENSION == ".html":
            if not (link.endswith(".html") or link.startswith("http")):
                link += ".html"
            return f"<a href=\"{link}\">{name}</a>"
        return f"[{name}]({link})"

    def md_link_converter(self, link: str, name: str) -> str:
        if link.startswith("id:"):
            hash = link[3:]
            roam_node = self.roam.id2node(hash)
            if roam_node is not None:
                return self.link(roam_node.base_name(), name)
                # return f"[[{roam_node.base_name()}]]"
            return link(name, name)
        return self.link(link, name)

    def handle_file(self, org_file: str, md_file: str) -> None:
        print(f"Processing file: {org_file} -> {md_file}")
        with open(md_file, "w", encoding="utf-8") as md_file_obj:
            for line in export(org_file, self.md_link_converter, self.roam):
                md_file_obj.write(line + "\n")

    def handle_folder(self, source_base: str, folder: str) -> None:
        for file in os.listdir(os.path.join(source_base, folder)):
            if file.endswith(".org"):
                print(f"{file}...")
                md_filename = os.path.splitext(file)[0] + EXTENSION
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
    converter = MarkdownConverter(roam_db)

    for file in roam_db.files:
        md_filename = os.path.join("tmp", file.replace(".org", EXTENSION))
        org_filename = "c:/home/jari/org-roam/" + file
        converter.handle_file(org_filename, md_filename)


if __name__ == "__main__":
    main()
