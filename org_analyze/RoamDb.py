import sqlite3
import os
from typing import List

def unquote(s: str) -> str:
    if s.startswith("\"") and s.endswith("\""):
        return s[1:-1]
    return s

class RoamNode:
    def __init__(self, id: str, title: str, file: str):
        self.id = id[1:-1]
        self.title = unquote(title)
        self.file = unquote(file)

    def base_name(self) -> str:
        return os.path.splitext(os.path.basename(self.file))[0]

    def __str__(self):
        return f"Node(id='{self.id}', title='{self.title}', file='{self.file}')"

class RoamLink:
    def __init__(self, source: str, destination: str, type: str):
        self.source = unquote(source)
        self.destination = unquote(destination)
        self.type = type


class RoamDB:
    def __init__(self, org_path: str):
        self.nodes: List[RoamNode] = []
        self.files: List[str] = []
        self.links: List[RoamLink] = []
        self.org_path = org_path

    def load(self, db_path: str):
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, title, file FROM nodes;")
            rows = cursor.fetchall()
            self.nodes = [RoamNode(row[0], row[1], self.convert_filename(unquote(row[2]))) for row in rows]

            cursor.execute("SELECT file FROM files;")
            rows = cursor.fetchall()
            self.files = [self.convert_filename(unquote(row[0])) for row in rows]

            cursor.execute("SELECT source, dest, type FROM links;")
            rows = cursor.fetchall()
            self.links = [RoamLink(row[0], row[1], row[2]) for row in rows]

    def get_files(self):
        return [fname for fname in self.files]

    def filename2id(self, filename: str):
        return next(
            (node.id for node in self.nodes if node.file == filename or self.convert_filename(node.file) == filename),
            None
        )

    def id2node(self, node_id: str) -> RoamNode:
        return next((node for node in self.nodes if node.id == node_id), None)

    def get_links(self, filename: str):
        rel_filename = self.convert_filename(filename)
        node_id = self.filename2id(rel_filename)
        if node_id is None:
            return []
        a = [self.id2node(link.destination) for link in self.links if link.source == node_id]
        b = [self.id2node(link.source) for link in self.links if link.destination == node_id]

        a.extend(b)
        return [node for node in a if node is not None]

    def convert_filename(self, filename: str) -> str:
        if filename.startswith(self.org_path):
            return filename[len(self.org_path) :]
        return filename
