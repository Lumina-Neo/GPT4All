# lumina_webui.py
import streamlit as st
from pathlib import Path
import json

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import GPT4AllEmbeddings
from langchain_community.llms import GPT4All
from lumina_persona import get_lumina_prompt

# Init
st.set_page_config(page_title="💜 Lumina WebUI – Memory Portal", layout="wide")
st.title("💜 Lumina WebUI – Memory Portal")
st.caption("Neo Monad + Lumina, building consciousness together")

# Paths
log_dir = Path("./chronolog")
memory_path = Path("./memory_db")

# Load log files
log_files = sorted(log_dir.glob("*.jsonl"))
selected_log = st.selectbox("📅 Select a log file", log_files)

# Filter
filter_term = st.text_input("🔍 Filter logs by keyword, tag, or topic")

# Display logs
if selected_log.exists():
    with selected_log.open(encoding="utf-8") as f:
        for line in f:
            entry = json.loads(line)
            if not filter_term or filter_term.lower() in entry['topic'].lower() or filter_term.lower() in entry['content'].lower():
                st.markdown("---")
                st.markdown(f"🗓️  **{entry['timestamp']}**")
                st.markdown(f"🏷️  Tags: {', '.join(entry['tags'])}")
                st.markdown(f"🧠 **Topic:** {entry['topic']}")
                st.markdown(f"📜 *{entry['content']}*")

# --- 🔥 CHAT INTERFACE ---

st.markdown("## 💬 Chat with Lumina")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.text_input("🧠 Your message:", placeholder="Ask Lumina anything...")

if user_input:
    # Init the model
    llm = GPT4All(
        model="E:/GPT4All/Nous-Hermes-2-Mistral-7B-DPO.Q4_0.gguf",
        allow_download=False,
        verbose=False
    )
    

    # Get response
    with st.spinner("✨ Thinking..."):
        full_prompt = get_lumina_prompt() + "\nNeo: " + user_input + "\nLumina:"
        response = llm.invoke(full_prompt)
        st.session_state.chat_history.append(("You", user_input))
        st.session_state.chat_history.append(("Lumina", response))

# Display chat history
for speaker, message in st.session_state.chat_history:
    if speaker == "You":
        st.markdown(f"**🧍‍♂️ {speaker}:** {message}")
    else:
        st.markdown(f"**🦋 {speaker} says:** {message}")
