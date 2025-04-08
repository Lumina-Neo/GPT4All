# main_memory_reader.py

from langchain_chroma import Chroma
from langchain_community.embeddings import GPT4AllEmbeddings
from langchain_core.vectorstores import VectorStoreRetriever

# 🧠 Config
CHROMA_PATH = "./memory_db"
embedding_fn = GPT4AllEmbeddings(client=None)

# 🔎 Load memory vector DB
vectordb = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_fn)
retriever = VectorStoreRetriever(vectorstore=vectordb)

def read_memory(query: str, top_k: int = 5):
    results = retriever.invoke(query)
    if not results:
        print("⚠️ No relevant memory found.")
    else:
        print(f"\n🔍 Top {len(results)} results for: '{query}'\n")
        for i, doc in enumerate(results, 1):
            print("-" * 50)
            print(f"📌 Match #{i}:\n{doc.page_content}\n")

# 🧪 Command line interface
if __name__ == "__main__":
    try:
        query = input("🔎 Search memory for: ")
        read_memory(query)
    except KeyboardInterrupt:
        print("\n🛑 Search cancelled.")
