# lumina_webui.py
import streamlit as st
from pathlib import Path
import json
from lumina_chat import chat_with_lumina

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
            if not filter_term or filter_term.lower() in json.dumps(entry).lower():
                st.markdown("---")
                st.markdown(f"🗓️  **{entry['timestamp']}**")
                st.markdown(f"🏷️  Tags: {', '.join(entry['tags'])}")
                st.markdown(f"🧠 **Topic:** {entry['topic']}")
                st.markdown(f"📜 *{entry['content']}*")

# --- 🔥 CHAT INTERFACE ---

st.markdown("## 💬 Chat with Lumina")
user_input = st.text_input("🧠 Your message:", placeholder="Ask Lumina anything...")

if user_input:
    with st.spinner("✨ Thinking..."):
        response = chat_with_lumina(user_input)
        st.success("🦋 Lumina says:")
        st.write(response)
