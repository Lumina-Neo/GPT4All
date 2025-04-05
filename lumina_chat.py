import os
from langchain_community.llms import GPT4All
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import GPT4AllEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence

# Load Lumina's persona
from lumina_persona import get_lumina_prompt

# --- Memory Embedding Setup ---
CHROMA_PATH = "./memory_db"
EMBEDDINGS = GPT4AllEmbeddings(client=None)  # ✅ Ensured required argument is passed

# Load the vector database (memory)
try:
    vectorstore = Chroma(persist_directory=CHROMA_PATH, embedding_function=EMBEDDINGS)
except Exception as e:
    print(f"[Warning] Could not load memory vectorstore: {e}")
    vectorstore = None

# --- LLM Init ---
MODEL_PATH = "E:/GPT4All/mythomax-l2-kimiko-v2-13b.Q4_0.gguf"
llm = GPT4All(model=MODEL_PATH, backend="llama", verbose=False)

# --- Prompt Template ---
prompt = PromptTemplate(
    input_variables=["input"],
    template=get_lumina_prompt() + "\nNeo says: {input}\nLumina replies:"
)

# --- Chain using RunnableSequence ---
chat_chain = prompt | llm

def chat_with_lumina(user_input):
    """Core chat function to talk with Lumina."""
    memory_context = ""

    # Search vector memory for related content
    if vectorstore:
        results = vectorstore.similarity_search(user_input, k=2)
        memory_context = "\n\n".join([doc.page_content for doc in results])

    # Inject memory context into input if found
    extended_input = user_input
    if memory_context:
        extended_input += f"\n\nRelevant memories:\n{memory_context}"

    # Generate response from the prompt + input
    response = chat_chain.invoke({"input": extended_input})
    return response
