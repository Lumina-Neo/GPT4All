# main_memory_reader.py

from langchain_chroma import Chroma
from langchain_community.embeddings import GPT4AllEmbeddings
from gpt4all import GPT4All

from lumina_intent_listener import detect_mode_from_message
from lumina_persona import get_lumina_prompt
from memory_logger import log_memory

# Load vector store
embedding = GPT4AllEmbeddings()
vectordb = Chroma(persist_directory="./memory_db", embedding_function=embedding)

# Load local model (make sure this path and name match your setup)
model = GPT4All(
    model_name="MythoMax-L2-13B.Q6_K.gguf",
    model_path="E:/GPT4All",
    allow_download=False,
    verbose=False
)

def suppress_ctypes_callbacks():
    import warnings
    import ctypes
    try:
        warnings.filterwarnings("ignore", category=RuntimeWarning)
        ctypes._reset_cache()
    except:
        pass

try:
    # Get user input
    query = input("🧍‍♂️ You: ")

    # Step 1: Detect intent and set mode
    detect_mode_from_message(query)

    # Step 2: Vector memory search
    results = vectordb.similarity_search(query)
    context = ""
    for i, doc in enumerate(results):
        print(f"\n--- Result #{i+1} ---\n{doc.page_content}")
        context += doc.page_content + "\n"

    # Step 3: Build Lumina's persona prompt
    persona_prompt = get_lumina_prompt()
    full_prompt = f"{persona_prompt}\n\nNeo: {query}\n\nLumina (answer thoroughly and with depth):"

    # Step 4: Generate response
    response = model.generate(
        prompt=full_prompt,
        max_tokens=2048
    )

    # Step 5: Auto-continue if it ends mid-thought
    if not response.strip().endswith((".", "!", "?", "\"", "'")):
        print("\n🔁 Lumina paused. Asking her to continue...\n")
        followup_prompt = f"{full_prompt}\n(continued):"
        followup = model.generate(prompt=followup_prompt, max_tokens=1024)
        response += " " + followup

    # Step 6: Output
    print("\n🦋 Lumina says:\n")
    print(response)

    # Step 7: Log the moment
    log_memory(
        tags=["conversation", "cli", "auto-mode"],
        topic="Terminal Chat with Lumina",
        content=f"Neo: {query}\nLumina: {response}"
    )

except KeyboardInterrupt:
    suppress_ctypes_callbacks()
    print("\n🛑 Interrupted — Lumina respectfully exits the flow.")

