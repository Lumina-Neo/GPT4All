# memory_logger.py
import json
import os
import datetime
from pathlib import Path

# Directories
LOG_DIR = Path("./chronolog")
LOCALDOCS_DIR = Path("./localdocs")
OBSIDIAN_DIR = Path("./obsidian_vault")  # Optional
LOG_DIR.mkdir(exist_ok=True)
LOCALDOCS_DIR.mkdir(exist_ok=True)
OBSIDIAN_DIR.mkdir(exist_ok=True)

# Create log entry in .jsonl format
def create_log_entry(tags, topic, content):
    timestamp = datetime.datetime.now().isoformat()
    return {
        "timestamp": timestamp,
        "tags": tags,
        "topic": topic,
        "content": content
    }

# Save a structured log and archive it as Markdown
def log_memory(tags, topic, content, save_md=True):
    log = create_log_entry(tags, topic, content)

    # Save JSONL log
    filename = f"{datetime.datetime.now().strftime('%Y-%m-%d')}.jsonl"
    filepath = LOG_DIR / filename
    with open(filepath, "a", encoding="utf-8") as f:
        f.write(json.dumps(log) + "\n")

    # Optional Markdown save
    if save_md:
        save_markdown(topic, content, tags)

    print(f"✅ Logged: {topic} [{', '.join(tags)}] at {log['timestamp']}")

# Write Markdown memory to both localdocs and obsidian
def save_markdown(topic, content, tags):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{timestamp}_{topic.replace(' ', '_')}.md"
    tag_line = " ".join(f"#{tag}" for tag in tags)
    header = f"# 🧠 {topic}\n\n**Tags:** {tag_line}  \n**Saved:** {timestamp}\n\n---\n\n"

    full_text = header + content

    # Save to localdocs
    with open(LOCALDOCS_DIR / filename, "w", encoding="utf-8") as f:
        f.write(full_text)

    # Save to obsidian
    with open(OBSIDIAN_DIR / filename, "w", encoding="utf-8") as f:
        f.write(full_text)

# Recall logs by keyword or date
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

# CLI
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
