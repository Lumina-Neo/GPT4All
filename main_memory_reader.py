from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import GPT4AllEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from gpt4all import GPT4All  # NEW: Local model call

# Load vector store
embedding = GPT4AllEmbeddings()
vectordb = Chroma(persist_directory="./memory_db", embedding_function=embedding)

# Load local model
model = GPT4All("nous-hermes-2-mistral.Q4_0.gguf")  # update with your model path

# Step 1: Query the vector memory
query = "What is a Monad?"
results = vectordb.similarity_search(query)

print("\n🔍 Top result(s):")
context = ""
for i, doc in enumerate(results):
    print(f"\n--- Result #{i+1} ---\n{doc.page_content}")
    context += doc.page_content + "\n"

# Step 2: Feed memory into GPT for synthesis
prompt = f"Based on the following context, explain the concept of a Monad in depth:\n\n{context}\n\nAnswer:"
response = model.generate(
    prompt=prompt,
    max_tokens=2048,
    temperature=0.7,
    top_p=0.9,
    repeat_penalty=1.1,
)

print("\n🧠 Lumina's Answer:\n")
print(response)
