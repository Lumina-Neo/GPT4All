# memory_search_cli.py

import json
from datetime import datetime

MEMORY_FILE = "memory.json"


def load_memory():
    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print("Memory file not found.")
        return {}


def display_section(title, items):
    print(f"\n=== {title.upper()} ===")
    if not items:
        print("  (No entries yet.)")
    for i, item in enumerate(items, 1):
        print(f"{i}. {item}")


def search_memory(keyword):
    memory = load_memory()
    print(f"\n\U0001F50E Searching memory for: '{keyword}'")
    found = False
    for section in ["knowledge", "farsight_sessions", "system_notes"]:
        print(f"\n-- In {section} --")
        entries = memory.get(section, [])
        for i, entry in enumerate(entries, 1):
            entry_str = json.dumps(entry) if isinstance(entry, dict) else str(entry)
            if keyword.lower() in entry_str.lower():
                print(f"{i}. {entry_str}")
                found = True
    if not found:
        print("No matching entries found.")


def main():
    memory = load_memory()
    while True:
        print("\nWhat would you like to do?")
        print("1. View all memory")
        print("2. Search memory")
        print("3. Exit")
        choice = input("Enter your choice (1-3): ").strip()

        if choice == "1":
            display_section("Knowledge", memory.get("knowledge", []))
            display_section("Farsight Sessions", memory.get("farsight_sessions", []))
            display_section("System Notes", memory.get("system_notes", []))
        elif choice == "2":
            keyword = input("Enter keyword to search: ").strip()
            search_memory(keyword)
        elif choice == "3":
            print("\U0001F9E0 Memory closed.")
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()
