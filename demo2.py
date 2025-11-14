from org_analyze import export_markdown
import os
import sqlite3

nodes = []

class Node:
    def __init__(self, id: str, title: str, file: str):
        self.id = id[1:-1]
        self.title = title
        self.file = file

    def base_name(self) -> str:
        return os.path.splitext(os.path.basename(self.file))[0]

    def __str__(self):
        return f"Node(id='{self.id}', title='{self.title}', file='{self.file}')"


def md_link_converter(link: str, name: str) -> str:
    if link.startswith("id:"):
        hash = link[3:]
        roam_node = next((node for node in nodes if node.id == hash), None)
        if roam_node is not None:
            # print(roam_node)
            return f"[[{roam_node.base_name()}]]"
        return f"[[{name}]]"
    return f"[{name}]({link})"

def handle_file(org_file: str, md_file:str) -> None:
    print(f"Processing file: {org_file} -> {md_file}")
    with open(md_file, "w", encoding="utf-8") as md_file:
        for line in export_markdown(org_file, md_link_converter):
            md_file.write(line + "\n")

def handle_folder(source_base: str, folder: str) -> None:
    for file in os.listdir(os.path.join(source_base, folder)):
        if file.endswith(".org"):
            print(f"{file}...")
            md_filename = os.path.splitext(file)[0] + ".md"
            handle_file(
                os.path.join(source_base, folder, file),
                os.path.join("tmp", folder, md_filename))

def convert_filename(filename: str) -> str:
    prefix = "\"c:/home/jari/org-roam/"
    if filename.startswith(prefix):
        return filename[len(prefix):-1]
    return filename

conn = sqlite3.connect(os.path.join("..", ".emacs.d", "org-roam.db"))
cursor = conn.cursor()
cursor.execute("SELECT id, title, file FROM nodes;")
rows = cursor.fetchall()
nodes = [Node(row[0], row[1], row[2]) for row in rows]

cursor = conn.cursor()
cursor.execute("SELECT file FROM files;")
rows = cursor.fetchall()
files = [convert_filename(row[0]) for row in rows]
conn.close()
#[print(node) for node in nodes]
#[print(file) for file in files]

folders = set([file.split("/")[0] for file in files if ("/" in file)])

os.makedirs("tmp", exist_ok=True)
for folder in folders:
    print(f"Creating folder tmp/{folder}...")
    os.makedirs(os.path.join("tmp", folder.lstrip("/")), exist_ok=True)

for file in files:
    # print(f"Handling file: {file}...")
    md_filename = os.path.join("tmp", file.replace(".org", ".md"))
    org_filename = os.path.join("..", "org-roam", file)

    print(f"Processing file: {org_filename} -> {md_filename}...")
    handle_file(
        org_filename,
        md_filename)

#exit(0)
