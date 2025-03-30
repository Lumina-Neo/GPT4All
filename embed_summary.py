# embed_summary.py

from main_memory_summary import MAIN_MEMORY_SUMMARY
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import GPT4AllEmbeddings
from langchain_community.document_loaders import Document
import os
from datetime import datetime

# 🔧 Path to memory database
persist_directory = "./memory_db"

# 🧠 Initialize embedding function
embeddings = GPT4AllEmbeddings()

# 🧱 Connect to ChromaDB
vectordb = Chroma(persist_directory=persist_directory, embedding_function=embeddings)

# 📄 Flatten memory structure
def flatten_memory(summary_dict):
    docs = []
    for section, bullets in summary_dict.items():
        for item in bullets:
            content = f"{section} | {item}"
            doc = Document(page_content=content, metadata={
                "section": section,
                "timestamp": datetime.utcnow().isoformat()
            })
            docs.append(doc)
    return docs

# 🧾 Load and store memory
documents = flatten_memory(MAIN_MEMORY_SUMMARY)
vectordb.add_documents(documents)
vectordb.persist()

print("✅ Main Memory embedded from structured file.")
