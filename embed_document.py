# embed_document.py
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import GPT4AllEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Path to the file you want to embed
file_path = "E:\GPT4All\First Collection\Main Memory Chat Backup Full Summary.txt"

# Load and split the text
loader = TextLoader("E:/GPT4All/First Collection/Main Memory Chat Backup Full Summary.txt", encoding="utf-8")

documents = loader.load()

splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
docs = splitter.split_documents(documents)

# Initialize embeddings and database
embeddings = GPT4AllEmbeddings()
vectordb = Chroma(persist_directory="./memory_db", embedding_function=embeddings)

# Store in memory!
vectordb.add_documents(docs)
vectordb.persist()

print("🧠 Memory embedded and stored in ChromaDB.")
