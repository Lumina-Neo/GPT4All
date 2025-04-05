# main_memory_embedder.py

from memory_summary import MAIN_MEMORY_SUMMARY
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_community.embeddings import GPT4AllEmbeddings
from datetime import datetime

# 🧠 Config
CHROMA_PATH = "./memory_db"
embedding_fn = GPT4AllEmbeddings(client=None)
vectordb = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_fn)

# 🧾 Flatten memory dict into documents
def flatten_summary(summary):
    documents = []
    for section, entries in summary.items():
        for bullet in entries:
            documents.append(
                Document(
                    page_content=f"{section}: {bullet}",
                    metadata={"section": section, "timestamp": datetime.utcnow().isoformat()}
                )
            )
    return documents

# 💾 Store in vector DB
docs = flatten_summary(MAIN_MEMORY_SUMMARY)
vectordb.add_documents(docs)

print("✅ Summary memory embedded into ChromaDB.")
