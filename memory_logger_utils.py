import os
import json
import uuid
from datetime import datetime
from langchain_community.embeddings import GPT4AllEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Initialize embeddings and vector store
embedding_function = GPT4AllEmbeddings(client=None)
vectordb = Chroma(persist_directory="./memory_db", embedding_function=embedding_function)

# Set up text splitter
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)


def log_memory(tags, topic, content):
    """
    Log a memory entry with tags, topic, and content into the vector DB.
    """
    timestamp = datetime.utcnow().isoformat()
    metadata = {
        "timestamp": timestamp,
        "tags": tags,
        "topic": topic
    }
    doc = Document(page_content=content, metadata=metadata)
    chunks = splitter.split_documents([doc])
    vectordb.add_documents(chunks)
    print(f"✅ Logged: {topic} [{', '.join(tags)}] at {timestamp}")


def search_memory(query, top_k=5):
    """
    Search memory based on a text query.
    """
    results = vectordb.similarity_search_with_score(query, k=top_k)
    print("\n🔍 Search Results:")
    for i, (doc, score) in enumerate(results):
        print("-" * 50)
        print(f"Result {i+1} (Score: {score:.2f}):")
        print(f"Topic: {doc.metadata.get('topic')}")
        print(f"Tags: {', '.join(doc.metadata.get('tags', []))}")
        print(f"Timestamp: {doc.metadata.get('timestamp')}")
        print(f"Content: {doc.page_content}\n")


# Command-line interface
if __name__ == '__main__':
    import sys
    from ast import literal_eval

    if len(sys.argv) < 2:
        print("Usage: memory_logger.py [log|recall] <args>")
        sys.exit(1)

    command = sys.argv[1].lower()

    if command == "log":
        if len(sys.argv) != 5:
            print("Usage: memory_logger.py log <tags> <topic> <content>")
            sys.exit(1)
        tags = literal_eval(sys.argv[2]) if sys.argv[2].startswith("[") else [t.strip() for t in sys.argv[2].split(',')]
        topic = sys.argv[3]
        content = sys.argv[4]
        log_memory(tags, topic, content)

    elif command == "recall":
        if len(sys.argv) < 3:
            print("Usage: memory_logger.py recall <query>")
            sys.exit(1)
        query = " ".join(sys.argv[2:])
        search_memory(query)

    else:
        print("Unknown command. Use 'log' or 'recall'.")
