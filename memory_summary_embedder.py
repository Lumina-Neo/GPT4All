# memory_summary_embedder.py

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_community.embeddings import GPT4AllEmbeddings
from memory_summary import MAIN_MEMORY_SUMMARY
from datetime import datetime

# 📍 Setup
CHROMA_PATH = "./memory_db"
embedding_fn = GPT4AllEmbeddings(client=None)
vectordb = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_fn)

# 📄 Flatten and embed
def flatten_summary(summary):
    docs = []
    for section, bullets in summary.items():
        for item in bullets:
            content = f"{section} | {item}"
            doc = Document(page_content=content, metadata={
                "section": section,
                "timestamp": datetime.utcnow().isoformat()
            })
            docs.append(doc)
    return docs

if __name__ == "__main__":
    print("🧠 Embedding structured summary into vector memory...")
    documents = flatten_summary(MAIN_MEMORY_SUMMARY)
    vectordb.add_documents(documents)
    print("✅ Summary embedded successfully.")
