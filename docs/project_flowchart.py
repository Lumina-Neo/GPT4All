# project_flowchart.py

import os
import os
os.environ["PATH"] += os.pathsep + r"C:\Program Files\Graphviz 2.44.1\bin"

from graphviz import Digraph
from pathlib import Path
import os

# Include only files we care about
INCLUDE_EXTENSIONS = {".py", ".md", ".txt"}
EXCLUDE_DIRS = {".git", "__pycache__", "langchain_env", "memory_db"}


def collect_relevant_files(root="."):
    file_nodes = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
        for file in filenames:
            ext = Path(file).suffix
            if ext in INCLUDE_EXTENSIONS:
                rel_path = os.path.relpath(os.path.join(dirpath, file), root)
                file_nodes.append(rel_path)
    return sorted(file_nodes)


def generate_flowchart(file_list, output_file="project_flowchart", format="png"):
    dot = Digraph(comment="Lumina Project Structure", format=format)
    dot.attr(rankdir="LR", fontsize="12")

    for file_path in file_list:
        parts = Path(file_path).parts
        for i in range(len(parts)):
            parent = " / ".join(parts[:i]) or "."
            current = " / ".join(parts[:i+1])
            if i < len(parts) - 1:
                dot.node(current, current.split(" / ")[-1], shape="folder")
            else:
                dot.node(current, current.split(" / ")[-1], shape="note")
            if i > 0:
                dot.edge(parent, current)

    dot.render(output_file, cleanup=True)
    print(f"✅ Flowchart saved as {output_file}.{format}")


if __name__ == "__main__":
    files = collect_relevant_files()
    generate_flowchart(files)
