# memory_log_and_embed.py

from memory_logger import log_memory as log_backup
from memory_logger_utils import log_memory as log_vector

def log_and_embed(tags, topic, content):
    """
    Logs memory to both:
    - Markdown + JSONL backup (via memory_logger)
    - Chroma vector DB (via memory_logger_utils)
    """
    print("\n🧠 Logging to human-readable backup...")
    log_backup(tags, topic, content)

    print("\n🔮 Embedding into vector memory...")
    log_vector(tags, topic, content)

    print("\n✅ Memory successfully logged and embedded.")

# CLI usage
if __name__ == "__main__":
    import sys
    from ast import literal_eval

    if len(sys.argv) != 4:
        print("Usage: memory_log_and_embed.py <tags> <topic> <content>")
        print("Example: python memory_log_and_embed.py \"[tag1,tag2]\" \"Topic\" \"Memory content...\")")
        sys.exit(1)

    tags = literal_eval(sys.argv[1]) if sys.argv[1].startswith("[") else [t.strip() for t in sys.argv[1].split(',')]
    topic = sys.argv[2]
    content = sys.argv[3]

    log_and_embed(tags, topic, content)
