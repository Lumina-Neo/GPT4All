# memory_vector_writer.py (Merged + Optimized)
# Keep this one

from datetime import datetime
from langchain_chroma import Chroma
from langchain_community.embeddings import GPT4AllEmbeddings
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

# --- Config ---
CHROMA_PATH = "./memory_db"
EMBEDDINGS = GPT4AllEmbeddings(client=None)
VSTORE = Chroma(persist_directory=CHROMA_PATH, embedding_function=EMBEDDINGS)
SPLITTER = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)

# --- Core Function ---
def log_to_vector_memory(tags, topic, content):
    timestamp = datetime.utcnow().isoformat()
    metadata = {
        "timestamp": timestamp,
        "tags": tags,
        "topic": topic
    }
    doc = Document(page_content=content, metadata=metadata)
    chunks = SPLITTER.split_documents([doc])
    VSTORE.add_documents(chunks)
    VSTORE.persist()
    print(f"✅ Vector memory embedded: {topic} [{', '.join(tags)}] @ {timestamp}")

# --- Search Function ---
def search_memory(query, k=5):
    results = VSTORE.similarity_search_with_score(query, k=k)
    print("\n🔍 Search Results:\n" + "-" * 50)
    for doc, score in results:
        ts = doc.metadata.get("timestamp", "[no timestamp]")
        print(f"🧠 {doc.metadata.get('topic', 'Unknown')} ({ts})")
        print(f"Tags: {', '.join(doc.metadata.get('tags', []))}")
        print(f"Relevance: {score:.2f}\nContent: {doc.page_content}\n")

# --- CLI Interface ---
if __name__ == "__main__":
    import sys
    from ast import literal_eval

    if len(sys.argv) < 2:
        print("Usage: memory_vector_writer.py [log/search] <args...>")
        exit(1)

    command = sys.argv[1].lower()

    if command == "log":
        if len(sys.argv) != 5:
            print("Usage: memory_vector_writer.py log '<topic>' '[tag1,tag2]' '<content>'")
            exit(1)
        topic = sys.argv[2]
        tags = literal_eval(sys.argv[3])
        content = sys.argv[4]
        log_to_vector_memory(tags, topic, content)

    elif command == "search":
        if len(sys.argv) != 3:
            print("Usage: memory_vector_writer.py search '<query>'")
            exit(1)
        query = sys.argv[2]
        search_memory(query)

    else:
        print(f"Unknown command: {command}")
