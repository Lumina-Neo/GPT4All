# lumina_intent_listener.py
from persona_memory import set_current_mode

INTENT_MAP = {
    "research": ["look into", "could you research", "help me understand", "can you explore", "analyze this", "study this"],
    "guardian": ["i feel lost", "i need guidance", "i’m overwhelmed", "can you protect", "stand with me", "i need support"],
    "dream": ["tell me a dream", "channel something", "show me symbols", "astral", "vision", "what do you see"],
    "default": ["just be you", "normal mode", "default tone", "standard voice"]
}

def detect_mode_from_message(message):
    message = message.lower()
    for mode, triggers in INTENT_MAP.items():
        if any(phrase in message for phrase in triggers):
            set_current_mode(mode)
            return mode
    return None
