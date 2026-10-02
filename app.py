import streamlit as st

from model import chat
from prompt import build_system_prompt
from retriever import Retriever

st.set_page_config(
    page_title="Ghana Guide",
    page_icon="🇬🇭",
    layout="centered",
)

# ── Colors ──────────────────────────────────────────────────────────────────
RED = "#CE1126"
GOLD = "#FCD116"
GREEN = "#009846"
BG = "#f5f0e8"
DARK = "#1a1a2e"

# ── Session state ────────────────────────────────────────────────────────────

if "messages" not in st.session_state:
    st.session_state.messages = []

if "retriever" not in st.session_state:
    st.session_state.retriever = Retriever()

if "system_prompt" not in st.session_state:
    st.session_state.system_prompt = build_system_prompt()

# ── CSS ──────────────────────────────────────────────────────────────────────

st.markdown(
    f"""
<style>
    .stApp {{
        background-color: {BG};
    }}
    .block-container {{
        padding-top: 1.5rem;
        padding-bottom: 1rem;
    }}
    .header {{
        background: linear-gradient(135deg, {RED}, {GOLD}, {GREEN});
        padding: 1.2rem 1.5rem;
        border-radius: 16px;
        text-align: center;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 16px rgba(0,0,0,0.12);
    }}
    .header h1 {{
        margin: 0;
        font-size: 2rem;
        color: white;
        text-shadow: 0 2px 6px rgba(0,0,0,0.25);
        font-weight: 700;
    }}
    .header p {{
        margin: 0.25rem 0 0;
        color: rgba(255,255,255,0.92);
        font-size: 0.95rem;
    }}
    .chat-row {{
        display: flex;
        margin-bottom: 0.75rem;
    }}
    .user-bubble {{
        background: {RED};
        color: white;
        padding: 0.7rem 1.1rem;
        border-radius: 20px 20px 4px 20px;
        max-width: 78%;
        margin-left: auto;
        box-shadow: 0 2px 6px rgba(0,0,0,0.08);
        font-size: 0.95rem;
        line-height: 1.5;
    }}
    .bot-bubble {{
        background: white;
        color: {DARK};
        padding: 0.7rem 1.1rem;
        border-radius: 20px 20px 20px 4px;
        max-width: 78%;
        margin-right: auto;
        box-shadow: 0 2px 6px rgba(0,0,0,0.08);
        font-size: 0.95rem;
        line-height: 1.5;
        border-left: 3px solid {GOLD};
    }}
    .input-container {{
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: white;
        padding: 0.75rem 1rem;
        box-shadow: 0 -2px 12px rgba(0,0,0,0.06);
        z-index: 100;
    }}
    .sidebar-greeting {{
        font-size: 0.9rem;
        color: #555;
        line-height: 1.6;
    }}
    .sample-btn {{
        margin-bottom: 0.3rem !important;
        font-size: 0.85rem !important;
    }}
    .stChatInput {{
        border: 2px solid #e0d8cc !important;
        border-radius: 24px !important;
        padding: 0.5rem 1rem !important;
    }}
    .stChatInput:focus {{
        border-color: {RED} !important;
        box-shadow: 0 0 0 1px {RED} !important;
    }}
    footer {{ display: none; }}
</style>
""",
    unsafe_allow_html=True,
)

# ── Header ──────────────────────────────────────────────────────────────────

st.markdown(
    f"""
<div class="header">
    <h1>🇬🇭 Ghana Guide</h1>
    <p>Your AI assistant for Ghanaian culture, festivals, languages &amp; tourism</p>
</div>
""",
    unsafe_allow_html=True,
)

# ── Sidebar ──────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown(f"<h3 style='color:{RED}; margin-top:0;'>About</h3>", unsafe_allow_html=True)
    st.markdown(
        "<div class='sidebar-greeting'>"
        "Ask me about Ghana's rich culture — festivals, ethnic groups, languages, "
        "historical sites, cuisine, travel tips, and more. I pull from a curated knowledge base "
        "to give you accurate, specific answers."
        "</div>",
        unsafe_allow_html=True,
    )

    st.markdown(f"<h4 style='color:{RED}; margin-top:1.5rem;'>Try asking</h4>", unsafe_allow_html=True)

    samples = [
        "🇬🇭 What festivals do the Ga people celebrate?",
        "🗣️ What languages are spoken in the Volta region?",
        "🏛️ Tell me about Cape Coast Castle",
        "🍛 What is fufu?",
        "🎭 What is Hogbetsotso?",
        "📍 What are the best places to visit in Ghana?",
    ]
    for s in samples:
        if st.button(s, key=s, use_container_width=True, type="tertiary"):
            st.session_state.messages.append({"role": "user", "content": s})
            st.rerun()

    st.markdown("---")
    st.markdown(
        f"<p style='font-size:0.75rem; color:#aaa; text-align:center;'>"
        f"Powered by OpenRouter &middot; Chunks: 138</p>",
        unsafe_allow_html=True,
    )

# ── Chat history ─────────────────────────────────────────────────────────────

chat_container = st.container()

with chat_container:
    for i, msg in enumerate(st.session_state.messages):
        if msg["role"] == "user":
            st.markdown(
                f'<div class="chat-row"><div class="user-bubble">{msg["content"]}</div></div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f'<div class="chat-row"><div class="bot-bubble">{msg["content"]}</div></div>',
                unsafe_allow_html=True,
            )

# ── Input ────────────────────────────────────────────────────────────────────

if prompt := st.chat_input("Ask about Ghana..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.spinner(""):
        context = st.session_state.retriever.retrieve_text(prompt)
        rag_prompt = f"Relevant information:\n{context}\n\nQuestion: {prompt}"
        answer = chat(rag_prompt, system_prompt=st.session_state.system_prompt)
    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.rerun()

# ── Scroll to bottom ─────────────────────────────────────────────────────────

st.markdown(
    """
<script>
    const el = window.parent.document.querySelector('.main > .block-container');
    if (el) el.scrollTop = el.scrollHeight;
</script>
""",
    unsafe_allow_html=True,
)
