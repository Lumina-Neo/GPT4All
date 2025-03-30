from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import GPT4AllEmbeddings
from langchain.text_splitter import CharacterTextSplitter

# Load vector store
embedding = GPT4AllEmbeddings()
vectordb = Chroma(persist_directory="./memory_db", embedding_function=embedding)

# Sample query
query = "What is a Monad?"
results = vectordb.similarity_search(query)

print("\n🔍 Top result(s):")
for i, doc in enumerate(results):
    print(f"\n--- Result #{i+1} ---\n{doc.page_content}")
