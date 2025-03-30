import json
from datetime import datetime
import os

# Path to your memory log
log_file = "E:/GPT4All/memory_log.json"

def load_log():
    if os.path.exists(log_file):
        with open(log_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_log(log_entries):
    with open(log_file, "w", encoding="utf-8") as f:
        json.dump(log_entries, f, indent=2)

def log_message(message):
    log_entries = load_log()
    entry = {
        "timestamp": datetime.now().isoformat(),
        "message": message
    }
    log_entries.append(entry)
    save_log(log_entries)
    print(f"📝 Logged: {message}")

if __name__ == "__main__":
    message = input("What do you want to log? ")
    log_message(message)
