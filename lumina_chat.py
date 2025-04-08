import os
from typing import Optional
from langchain_community.llms import GPT4All
from langchain_chroma import Chroma
from langchain_community.embeddings import GPT4AllEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence
from langchain_core.vectorstores import VectorStoreRetriever

from lumina_persona import get_lumina_prompt
from memory_logger import log_memory
from memory_vector_writer import log_to_vector_memory
from core_summary_manager import load_summary, embed_summary

# --- Config ---
CHROMA_PATH = "./memory_db"
MODEL_PATH = "E:/GPT4All/mythomax-l2-kimiko-v2-13b.Q4_0.gguf"

# --- Initialization ---
vectorstore: Optional[Chroma] = None
retriever: Optional[VectorStoreRetriever] = None
chat_chain: Optional[RunnableSequence] = None

# --- Embeddings and Vectorstore ---
EMBEDDINGS = GPT4AllEmbeddings(client=None)
try:
    vectorstore = Chroma(persist_directory=CHROMA_PATH, embedding_function=EMBEDDINGS)
    retriever = VectorStoreRetriever(vectorstore=vectorstore)
except Exception as e:
    print(f"[Warning] Could not load memory vectorstore: {e}")

# --- Embed Core Summary Memory on Boot ---
try:
    core_summary = load_summary()
    embed_summary(core_summary)
    print("✅ Core summary loaded and embedded.")
except Exception as e:
    print(f"[Warning] Could not embed core summary: {e}")

# --- LLM and Prompt Setup ---
llm = GPT4All(model=MODEL_PATH, backend="llama", verbose=False)
prompt = PromptTemplate(
    input_variables=["input"],
    template=get_lumina_prompt() + "\nNeo says: {input}\nLumina replies:"
)
chat_chain = prompt | llm

# --- Core Chat Function ---
def chat_with_lumina(user_input):
    """Talk with Lumina, embed and log memory, return response."""
    memory_context = ""

    if retriever:
        results = retriever.invoke(user_input)
        memory_context = "\n\n".join([doc.page_content for doc in results])

    extended_input = user_input
    if memory_context:
        extended_input += f"\n\nRelevant memories:\n{memory_context}"

    response = chat_chain.invoke({"input": extended_input}) if chat_chain else "[Error: chat_chain not available]"

    topic = "User Conversation"
    tags = ["chat", "lumina", "live"]
    content = f"User: {user_input}\nLumina: {response}"

    if vectorstore:
        log_to_vector_memory(tags, topic, content)
    log_memory(tags, topic, content)

    return response
