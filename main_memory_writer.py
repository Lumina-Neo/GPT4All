# main_memory_writer.py (Final Polished Version)

from langchain_chroma import Chroma
from langchain_community.embeddings import GPT4AllEmbeddings
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from datetime import datetime

# 🔧 Config
CHROMA_PATH = "./memory_db"
embedding_fn = GPT4AllEmbeddings(client=None)
vectordb = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_fn)
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)

def write_memory(topic: str, tags: list[str], content: str):
    timestamp = datetime.utcnow().isoformat()
    metadata = {
        "topic": topic,
        "tags": tags,
        "timestamp": timestamp,
    }
    doc = Document(page_content=content, metadata=metadata)
    chunks = splitter.split_documents([doc])
    vectordb.add_documents(chunks)
    print(f"✅ Memory written: {topic} [{', '.join(tags)}] at {timestamp}")

# 🧪 Example usage
if __name__ == "__main__":
    import sys
    from ast import literal_eval

    if len(sys.argv) != 4:
        print("Usage: python main_memory_writer.py '<topic>' '[tag1,tag2]' '<content>'")
        sys.exit(1)

    topic = sys.argv[1]
    tags = literal_eval(sys.argv[2])
    content = sys.argv[3]

    write_memory(topic, tags, content)
