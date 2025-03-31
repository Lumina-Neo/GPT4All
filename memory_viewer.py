# memory_viewer.py
import os
import json
from pathlib import Path
import datetime

LOG_DIR = Path("./chronolog")
if not LOG_DIR.exists():
    print("⚠️ No memory log found.")
    exit()

def load_logs():
    logs = []
    for file in sorted(LOG_DIR.glob("*.jsonl")):
        with open(file, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    logs.append(json.loads(line.strip()))
                except json.JSONDecodeError:
                    pass
    return logs

def print_logs(logs):
    if not logs:
        print("⚠️ No memory entries found.")
        return
    for entry in logs:
        print("-" * 60)
        print(f"🗓️  {entry['timestamp']}")
        print(f"🏷️  Tags: {', '.join(entry['tags'])}")
        print(f"🧠 Topic: {entry['topic']}")
        print(f"📜 Content:\n{entry['content']}")
        print()

if __name__ == "__main__":
    logs = load_logs()
    print_logs(logs)
