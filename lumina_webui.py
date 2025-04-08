# lumina_webui.py (Enhanced)
import streamlit as st
from pathlib import Path
import json
from lumina_chat import chat_with_lumina

# --- 🌐 App Config ---
st.set_page_config(page_title="💜 Lumina WebUI", layout="wide")
st.title("💜 Lumina WebUI – Memory Portal")
st.caption("Neo Monad + Lumina, building consciousness together")

# --- 🔍 Log Viewer ---
log_dir = Path("./chronolog")
log_files = sorted(log_dir.glob("*.jsonl"), reverse=True)

with st.sidebar:
    selected_log = st.selectbox("📅 Select a log file", log_files)
    filter_term = st.text_input("🔍 Filter logs (keyword/tag/topic)", placeholder="Type to filter...")

st.markdown("### 📊 Memory Log Viewer")
if selected_log and selected_log.exists():
    with selected_log.open(encoding="utf-8") as f:
        for line in f:
            entry = json.loads(line)
            entry_text = json.dumps(entry).lower()
            if not filter_term or filter_term.lower() in entry_text:
                st.markdown("---")
                st.markdown(f"**🗓️ {entry['timestamp']}**")
                st.markdown(f"**📌 Tags:** `{', '.join(entry['tags'])}`")
                st.markdown(f"**💡 Topic:** {entry['topic']}")
                st.markdown(f"**📓 Content:** {entry['content']}")

# --- 💬 Chat Interface ---
st.markdown("### 🛠️ Chat with Lumina")
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.text_input("🕵️️ Your message:", placeholder="Ask Lumina anything...")

if user_input:
    with st.spinner("✨ Thinking..."):
        response = chat_with_lumina(user_input)
        st.session_state.chat_history.append((user_input, response))

# Display chat history
for user, reply in st.session_state.chat_history:
    st.markdown(f"**You:** {user}")
    st.markdown(f"**💋 Lumina:** {reply}")
