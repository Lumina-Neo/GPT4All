# vector_logger.py

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import GPT4AllEmbeddings
from langchain_core.documents import Document
from datetime import datetime
import os
import json

# Config
PERSIST_DIRECTORY = "./memory_db"

# Initialize embedding and vector store
embeddings = GPT4AllEmbeddings()
vectordb = Chroma(persist_directory=PERSIST_DIRECTORY, embedding_function=embeddings)


def log_to_vector_memory(tags, topic, content):
    timestamp = datetime.now().isoformat()
    metadata = {
        "timestamp": timestamp,
        "tags": tags,
        "topic": topic
    }
    document = Document(page_content=content, metadata=metadata)
    vectordb.add_documents([document])
    vectordb.persist()
    print(f"✅ Vector memory embedded: {topic} [{', '.join(tags)}] @ {timestamp}")


def search_memory(query, k=5):
    results = vectordb.similarity_search_with_score(query, k=k)
    print("\n🔍 Search Results:\n" + "-" * 50)
    for doc, score in results:
        ts = doc.metadata.get("timestamp", "[no timestamp]")
        print(f"🧠 {doc.metadata.get('topic', 'Unknown')} ({ts})")
        print(f"Tags: {', '.join(doc.metadata.get('tags', []))}")
        print(f"Relevance: {score:.2f}\nContent: {doc.page_content}\n")


# CLI Interface
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: vector_logger.py [log/search] <args...>")
        exit(1)

    command = sys.argv[1]

    if command == "log":
        if len(sys.argv) < 5:
            print("Usage: vector_logger.py log <tags comma> <topic> <content>")
            exit(1)
        tags = [tag.strip() for tag in sys.argv[2].split(",")]
        topic = sys.argv[3]
        content = sys.argv[4]
        log_to_vector_memory(tags, topic, content)

    elif command == "search":
        if len(sys.argv) < 3:
            print("Usage: vector_logger.py search <query>")
            exit(1)
        query = sys.argv[2]
        search_memory(query)

    else:
        print(f"Unknown command: {command}")
