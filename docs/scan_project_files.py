import os

def scan_directory(path="."):
    file_map = {}
    for root, dirs, files in os.walk(path):
        rel_root = os.path.relpath(root, path)
        file_map[rel_root] = files
    return file_map

def main():
    project_path = "."  # or replace with specific path
    file_structure = scan_directory(project_path)

    with open("lumina_file_map.txt", "w", encoding="utf-8") as f:
        for folder, files in file_structure.items():
            f.write(f"\n📂 {folder}\n")
            for file in files:
                f.write(f"  └── {file}\n")
    
    print("[✔] File map written to lumina_file_map.txt")

if __name__ == "__main__":
    main()
