# main_memory_search.py

from langchain_chroma import Chroma
from langchain_community.embeddings import GPT4AllEmbeddings

# 📂 Path to vector database
CHROMA_PATH = "./memory_db"
embedding_fn = GPT4AllEmbeddings(client=None)
vectordb = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_fn)

def search_memory(query, top_k=5):
    results = vectordb.similarity_search_with_score(query, k=top_k)
    print(f"\n🔍 Search results for: '{query}'")
    for i, (doc, score) in enumerate(results, 1):
        print("-" * 50)
        print(f"Result {i} (Score: {score:.2f})")
        print(f"📄 {doc.page_content}")
        print(f"🧠 Meta: {doc.metadata}\n")

if __name__ == "__main__":
    try:
        user_query = input("Enter search query: ")
        search_memory(user_query)
    except KeyboardInterrupt:
        print("\n🛑 Search cancelled.")
