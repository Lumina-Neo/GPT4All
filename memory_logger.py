# memory_logger.py (Refactored)
# Keep this one
import json
import os
from datetime import datetime
from pathlib import Path

# 🔧 Directory setup
LOG_DIR = Path("./chronolog")
LOCALDOCS_DIR = Path("./localdocs")
OBSIDIAN_DIR = Path("./obsidian_vault")

for dir_path in [LOG_DIR, LOCALDOCS_DIR, OBSIDIAN_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)

# 🧾 JSONL log structure

def create_log_entry(tags, topic, content):
    return {
        "timestamp": datetime.now().isoformat(),
        "tags": tags,
        "topic": topic,
        "content": content
    }

def save_markdown(topic, content, tags):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{timestamp}_{topic.replace(' ', '_')}.md"
    header = f"# 🧠 {topic}\n\n**Tags:** {' '.join(f'#{tag}' for tag in tags)}  \\n**Saved:** {timestamp}\n\n---\n\n"
    full_text = header + content

    for target_dir in [LOCALDOCS_DIR, OBSIDIAN_DIR]:
        with open(target_dir / filename, "w", encoding="utf-8") as f:
            f.write(full_text)

def log_memory(tags, topic, content, save_md=True):
    log = create_log_entry(tags, topic, content)
    filename = f"{datetime.now().strftime('%Y-%m-%d')}.jsonl"
    filepath = LOG_DIR / filename

    with open(filepath, "a", encoding="utf-8") as f:
        f.write(json.dumps(log) + "\n")

    if save_md:
        save_markdown(topic, content, tags)

    print(f"✅ Logged: {topic} [{', '.join(tags)}] at {log['timestamp']}")

def recall_logs(keyword=None, date=None):
    logs = []
    files = [LOG_DIR / f"{date}.jsonl"] if date else sorted(LOG_DIR.glob("*.jsonl"))

    for file in files:
        with open(file, encoding="utf-8") as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    if not keyword or keyword.lower() in json.dumps(entry).lower():
                        logs.append(entry)
                except json.JSONDecodeError:
                    pass
    return logs

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: memory_logger.py [log|recall] <args>")
        sys.exit(1)

    command = sys.argv[1].lower()

    if command == "log" and len(sys.argv) == 5:
        tags = [tag.strip() for tag in sys.argv[2].split(",")]
        topic = sys.argv[3]
        content = sys.argv[4]
        log_memory(tags, topic, content)

    elif command == "recall":
        keyword = sys.argv[2] if len(sys.argv) > 2 else None
        results = recall_logs(keyword=keyword)
        for r in results:
            print("-" * 50)
            print(json.dumps(r, indent=2))
    else:
        print("Unknown or invalid command. Use 'log' or 'recall'.")
