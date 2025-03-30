from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import GPT4AllEmbeddings
from langchain_community.document_loaders import TextLoader

# Step 1: Set file path to your memory summary
file_path = "E:/GPT4All/First Collection/Main Memory Chat Backup Full Summary.txt"

# Step 2: Load the document
loader = TextLoader(file_path, encoding='utf-8')
documents = loader.load()

# Step 3: Set up the embedding model
embeddings = GPT4AllEmbeddings()

# Step 4: Connect to ChromaDB
vectordb = Chroma.from_documents(documents, embeddings, persist_directory="./memory_db")

# Step 5: Save the embedded memory
vectordb.persist()
print("✅ Main memory summary embedded successfully into vector memory.")
