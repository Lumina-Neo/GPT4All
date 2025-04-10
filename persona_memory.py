# persona_memory.py
from pathlib import Path

MODE_FILE = Path("./current_mode.txt")
VALID_MODES = {"default", "dream", "research", "guardian"}

def get_current_mode():
    if MODE_FILE.exists():
        return MODE_FILE.read_text().strip()
    return "default"

def set_current_mode(mode, verbose=True):
    mode = mode.strip().lower()
    if mode in VALID_MODES:
        MODE_FILE.write_text(mode)
        if verbose:
            print(f"🌀 Persona mode updated to: {mode}")
    else:
        if verbose:
            print(f"⚠️ Invalid mode: '{mode}' not in {VALID_MODES}")
