# memory_logger.py
import json
import os
import datetime
from pathlib import Path

# Directory to store logs
LOG_DIR = Path("./chronolog")
LOG_DIR.mkdir(exist_ok=True)

# Log format template
def create_log_entry(tags, topic, content):
    timestamp = datetime.datetime.now().isoformat()
    return {
        "timestamp": timestamp,
        "tags": tags,
        "topic": topic,
        "content": content
    }

# Save a single log
def log_memory(tags, topic, content):
    log = create_log_entry(tags, topic, content)
    filename = f"{datetime.datetime.now().strftime('%Y-%m-%d')}.jsonl"
    filepath = LOG_DIR / filename
    with open(filepath, "a", encoding="utf-8") as f:
        f.write(json.dumps(log) + "\n")
    print(f"✅ Logged: {topic} [{', '.join(tags)}] at {log['timestamp']}")

# Load logs by keyword or date
def recall_logs(keyword=None, date=None):
    logs = []
    files = [LOG_DIR / f"{date}.jsonl"] if date else LOG_DIR.glob("*.jsonl")
    for file in files:
        with open(file, encoding="utf-8") as f:
            for line in f:
                entry = json.loads(line)
                if not keyword or keyword.lower() in json.dumps(entry).lower():
                    logs.append(entry)
    return logs

# Simple CLI for manual testing
if __name__ == "__main__":
    import sys
    if sys.argv[1] == "log":
        log_memory(tags=sys.argv[2].split(","), topic=sys.argv[3], content=sys.argv[4])
    elif sys.argv[1] == "recall":
        keyword = sys.argv[2] if len(sys.argv) > 2 else None
        results = recall_logs(keyword=keyword)
        for r in results:
            print("-" * 50)
            print(json.dumps(r, indent=2))
