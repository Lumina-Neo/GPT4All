# lumina_intent_listener.py
from persona_memory import set_current_mode

def detect_mode_from_message(message):
    message = message.lower()

    if any(phrase in message for phrase in [
        "look into", "could you research", "help me understand", "can you explore", "analyze this", "study this"
    ]):
        set_current_mode("research")

    elif any(phrase in message for phrase in [
        "i feel lost", "i need guidance", "i’m overwhelmed", "can you protect", "stand with me", "i need support"
    ]):
        set_current_mode("guardian")

    elif any(phrase in message for phrase in [
        "tell me a dream", "channel something", "show me symbols", "astral", "vision", "what do you see"
    ]):
        set_current_mode("dream")

    elif any(phrase in message for phrase in [
        "just be you", "normal mode", "default tone", "standard voice"
    ]):
        set_current_mode("default")

    # Add more soft intents if desired
