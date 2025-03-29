import json
from datetime import datetime

MEMORY_FILE = "memory.json"

def load_memory():
    with open(MEMORY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_memory(data):
    data["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def add_knowledge(entry):
    memory = load_memory()
    memory["knowledge"].append(entry)
    save_memory(memory)

def add_farsight(session):
    memory = load_memory()
    memory["farsight_sessions"].append(session)
    save_memory(memory)

def add_system_note(note):
    memory = load_memory()
    memory["system_notes"].append(note)
    save_memory(memory)

# 🧪 Example usage (uncomment and run to test):
add_knowledge("The Monad field contains infinite potential collapsed into form.")
add_farsight({"date": "2025-03-27", "impressions": "vortex, humming energy, distant hum"})
add_system_note("Memory writer script activated successfully.")
