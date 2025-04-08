# project_structure_map.py

import os
from pathlib import Path
from collections import defaultdict

# 🎯 File types to track
INCLUDE_EXTENSIONS = {".py", ".txt", ".md"}
EXCLUDE_DIRS = {".git", "__pycache__", "langchain_env", "memory_db"}


def scan_files(root="."):
    project_map = defaultdict(list)

    for dirpath, dirnames, filenames in os.walk(root):
        # Filter out excluded directories
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]

        for file in filenames:
            ext = Path(file).suffix
            if ext in INCLUDE_EXTENSIONS:
                full_path = os.path.join(dirpath, file)
                rel_path = os.path.relpath(full_path, root)
                project_map[ext].append(rel_path)

    return project_map


def save_file_map(file_map, out_path="project_file_map.txt"):
    with open(out_path, "w", encoding="utf-8") as f:
        for ext, files in sorted(file_map.items()):
            f.write(f"\n# {ext.upper()} Files ({len(files)})\n")
            for file in sorted(files):
                f.write(f"- {file}\n")
    print(f"✅ File map saved to {out_path}")


if __name__ == "__main__":
    file_map = scan_files()
    save_file_map(file_map)
