# core_summary_manager.py

import json
from datetime import datetime
from langchain_chroma import Chroma
from langchain_community.embeddings import GPT4AllEmbeddings
from langchain_core.documents import Document

# 🔧 Config
SUMMARY_PATH = "main_memory_summary.json"
CHROMA_PATH = "./memory_db"

# 🧠 Load and save summary
def load_summary():
    with open(SUMMARY_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_summary(summary_dict):
    with open(SUMMARY_PATH, "w", encoding="utf-8") as f:
        json.dump(summary_dict, f, indent=2)

# ➕ Add a bullet to a section
def add_summary_bullet(section, bullet):
    summary = load_summary()
    if section in summary:
        summary[section].append(bullet)
    else:
        summary[section] = [bullet]
    save_summary(summary)
    embed_summary(summary)  # 🔁 Re-embed after update
    print(f"✅ Added bullet to '{section}': {bullet}")

# 🗑 Remove a bullet by index from a section
def remove_summary_bullet(section, index):
    summary = load_summary()
    try:
        removed = summary[section].pop(index)
        if not summary[section]:
            del summary[section]
        save_summary(summary)
        embed_summary(summary)  # 🔁 Re-embed after update
        print(f"🗑 Removed bullet #{index+1} from '{section}': {removed}")
    except (IndexError, KeyError):
        print(f"⚠️ Could not remove bullet. Section or index invalid.")

# 📦 Embed summary into Chroma vector DB
def embed_summary(summary_dict):
    embeddings = GPT4AllEmbeddings(client=None)
    vectordb = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)

    documents = []
    timestamp = datetime.utcnow().isoformat()

    for section, bullets in summary_dict.items():
        for bullet in bullets:
            documents.append(Document(
                page_content=f"{section}: {bullet}",
                metadata={"section": section, "timestamp": timestamp}
            ))

    vectordb.add_documents(documents)
    vectordb.persist()
    print(f"✅ Embedded {len(documents)} summary entries into vector memory.")
