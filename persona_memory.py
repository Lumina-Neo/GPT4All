# persona_memory.py
from pathlib import Path

MODE_FILE = Path("./current_mode.txt")

def get_current_mode():
    if MODE_FILE.exists():
        return MODE_FILE.read_text().strip()
    return "default"

def set_current_mode(mode):
    MODE_FILE.write_text(mode.strip())
    print(f"🌀 Persona mode updated to: {mode}")
