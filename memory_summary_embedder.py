# memory_summary_embedder.py (Final Version – Merged & Polished)
#Keep this one

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_community.embeddings import GPT4AllEmbeddings
from memory_summary import MAIN_MEMORY_SUMMARY
from datetime import datetime

# 📍 Setup
CHROMA_PATH = "./memory_db"
EMBEDDINGS = GPT4AllEmbeddings(client=None)
VECTORDDB = Chroma(persist_directory=CHROMA_PATH, embedding_function=EMBEDDINGS)

# 🔄 Flatten structured summary into vector-ready documents
def flatten_summary(summary):
    docs = []
    for section, bullets in summary.items():
        for item in bullets:
            content = f"{section}: {item}"
            doc = Document(
                page_content=content,
                metadata={
                    "section": section,
                    "timestamp": datetime.utcnow().isoformat()
                }
            )
            docs.append(doc)
    return docs

# 🚀 Run embedding when executed directly
if __name__ == "__main__":
    print("🧠 Embedding MAIN_MEMORY_SUMMARY into Chroma vector memory...")
    documents = flatten_summary(MAIN_MEMORY_SUMMARY)
    VECTORDDB.add_documents(documents)
    print("✅ Summary embedded successfully.")
