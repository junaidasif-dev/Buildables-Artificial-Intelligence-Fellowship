import os
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
from groq import Groq
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

# Resolve workspace root and load env
WORKSPACE = Path(__file__).resolve().parent.parent
WEEK03 = WORKSPACE / "Week-03"
ENV = WORKSPACE / ".env"
load_dotenv(ENV)
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    st.error("GROQ_API_KEY missing in .env at repo root")
    st.stop()
client = Groq(api_key=GROQ_API_KEY)

# Model aliases for backward compatibility
MODEL_ALIASES = {
    "llama3-8b-8192": "llama-3.1-8b-instant",
    "llama3-70b-8192": "llama-3.1-70b-versatile",
}

def normalize_model(model: str) -> str:
    return MODEL_ALIASES.get(model, model)

CORPUS = WEEK03 / "joni_eats_corpus.txt"

def read_text(p: Path) -> str:
    return p.read_text(encoding="utf-8")

def parse_corpus(corpus: str):
    import re
    sections = re.split(r"^### SECTION: (.+)$", corpus, flags=re.M)
    mapping = {"RESTAURANT_KB": "", "CHAT_PATTERNS": "", "CONTEXT_FLOW": ""}
    for i in range(1, len(sections), 2):
        name = sections[i].strip().upper()
        body = sections[i+1] if i+1 < len(sections) else ""
        if name in mapping:
            mapping[name] = body.strip()
    return mapping["RESTAURANT_KB"], mapping["CHAT_PATTERNS"], mapping["CONTEXT_FLOW"]

@st.cache_resource(show_spinner=False)
def init_assets():
    corpus = read_text(CORPUS)
    kb_text, patterns, flow = parse_corpus(corpus)
    return kb_text, patterns, flow

def split_chunks(text: str, min_len: int = 120):
    import re
    parts = [p.strip() for p in re.split(r"\n\s*\n+", text) if p.strip()]
    chunks = []
    for p in parts:
        if len(p) >= min_len:
            chunks.append(p)
        elif chunks and len(chunks[-1]) < min_len:
            chunks[-1] += "\n" + p
        else:
            chunks.append(p)
    return chunks

@st.cache_resource(show_spinner=False)
def init_retriever(kb_text: str):
    chunks = split_chunks(kb_text)
    vec = TfidfVectorizer(
        ngram_range=(1,3),
        stop_words="english",
        lowercase=True,
        strip_accents="unicode",
        sublinear_tf=True,
    )
    mat = vec.fit_transform(chunks)
    return vec, mat, chunks

# Note: We rely purely on retrieval; no special dietary indexing logic needed.

def retrieve(vec, mat, chunks, query: str, top_k: int = 5):
    qv = vec.transform([query])
    sims = cosine_similarity(qv, mat).ravel()
    idxs = sims.argsort()[::-1][:top_k]
    return [(int(i), float(sims[i]), chunks[int(i)]) for i in idxs]

def system_prompt():
    return (
        "You are Joni Eats’ cafe assistant. Be friendly, concise, and factual. "
        "Use only the provided context snippets as your source of truth. If the answer isn't in the context, say you're not sure and ask a brief follow-up. "
        "Scope: menu items (with ingredients/allergens when present), dietary suitability (vegan/vegetarian/gluten-free/halal), prices, hours, location, specials, ordering, and events. "
        "Style: short paragraphs; when listing items, use bullet points (max 5) and prefer the most relevant choices. "
        "When the user asks for a category (e.g., vegan/vegetarian/gluten-free/halal), scan the context and list matching items explicitly if present. "
        "Do not deny availability when the context shows relevant items. Do not invent items, ingredients, prices, or policies that aren't in the context. "
        "Maintain conversation context across messages; do not restart with greetings mid-conversation. If user preferences change (e.g., meat vs vegan), adapt recommendations accordingly. "
        "If asked for 'most selling' and it's not in context, suggest popular-looking combos or deals without claiming they are the top-selling. "
        "Avoid medical or legal advice; suggest speaking to staff for severe allergies or guarantees."
    )

MAX_HISTORY = 10

def _sanitize(text: str) -> str:
    text = text.strip()
    if len(text) > 1200:
        text = text[:1200] + "…"
    return text

def _history_messages(history):
    msgs = []
    if not history:
        return msgs
    # Keep the last MAX_HISTORY turns
    tail = history[-MAX_HISTORY:]
    for role, content in tail:
        if role in ("user", "assistant") and isinstance(content, str) and content.strip():
            msgs.append({"role": role, "content": _sanitize(content)})
    return msgs

def render_messages(sp: str, query: str, hits, few_shots: str | None, history=None):
    ctx = "\n\n".join([f"[Snippet {i}]\n{t}" for i,_s,t in hits])
    msgs = [
        {"role":"system","content": sp},
        {"role":"system","content": "Context from KB:\n" + (ctx or "(none)")},
    ]
    if few_shots and few_shots.strip():
        msgs.append({"role":"system","content":"Examples:\n" + few_shots.strip()})
    # Append short conversation history before current turn
    msgs.extend(_history_messages(history))
    msgs.append({"role":"user","content": query})
    return msgs

def answer(query, vec, mat, chunks, patterns, model, temperature, top_k, history=None):
    hits = retrieve(vec, mat, chunks, query, top_k=top_k)
    model = normalize_model(model)
    msgs = render_messages(system_prompt(), query, hits, patterns, history=history)
    resp = client.chat.completions.create(model=model, messages=msgs, temperature=temperature)
    text = resp.choices[0].message.content
    return text, hits

st.set_page_config(page_title="Joni Eats Chatbot", page_icon="🍽️", layout="wide")

# --- Custom Styles & Brand Header ---
st.markdown(
        """
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');
            :root { 
                --joni-primary: #FF5E8A; 
                --joni-accent: #FFD166; 
                --joni-bg1: #FFF5F7; 
                --joni-bg2: #F0F7FF; 
                --joni-card: #FFFFFF;
            }
            .stApp { 
                background: linear-gradient(180deg, var(--joni-bg1) 0%, var(--joni-bg2) 100%);
                font-family: 'Poppins', system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, "Apple Color Emoji", "Segoe UI Emoji";
            }
            .joni-hero { 
                padding: 24px 28px; border-radius: 16px; 
                background: radial-gradient(1200px 400px at top left, rgba(255,94,138,0.18), rgba(255,209,102,0.2)),
                                        linear-gradient(135deg, rgba(255,255,255,0.85), rgba(255,255,255,0.9));
                border: 1px solid rgba(0,0,0,0.06); box-shadow: 0 8px 30px rgba(31,41,55,0.08);
            }
            .joni-title { font-size: 30px; font-weight: 700; color: #111827; margin: 0; }
            .joni-sub { color: #475569; margin-top: 6px; }
            .joni-pill { display: inline-block; padding: 6px 12px; margin: 8px 8px 0 0; border-radius: 999px; 
                                     background: linear-gradient(135deg, rgba(255,94,138,0.12), rgba(255,209,102,0.12));
                                     color: #111827; border: 1px solid rgba(0,0,0,0.06); font-size: 12px; }
        </style>
        """,
        unsafe_allow_html=True,
)

st.markdown(
        """
        <div class="joni-hero">
            <div class="joni-title">🍽️ Welcome to Joni Eats</div>
            <div class="joni-sub">Quick, friendly answers about our menu, dietary options, hours, and specials.</div>
            <div style="margin-top:8px;">
                <span class="joni-pill">Fast answers</span>
                <span class="joni-pill">Dietary-friendly choices</span>
                <span class="joni-pill">Today’s hours</span>
                <span class="joni-pill">Specials & favorites</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
)

# Chat bubble styles (high contrast)
st.markdown(
        """
        <style>
            .chat-row { display: flex; margin: 8px 0; }
            .chat-row.user { justify-content: flex-start; }
            .chat-row.assistant { justify-content: flex-end; }
            .bubble { max-width: 75%; padding: 12px 14px; border-radius: 14px; box-shadow: 0 4px 16px rgba(17,24,39,0.06); }
            .bubble.user { background: #FFFFFF; color: #111827; border: 1px solid rgba(0,0,0,0.06); }
            .bubble.assistant { background: #111827; color: #F9FAFB; border: 1px solid rgba(0,0,0,0.2); }
            .bubble .meta { font-size: 12px; opacity: 0.7; margin-bottom: 6px; }
        </style>
        """,
        unsafe_allow_html=True,
)

kb_text, patterns, flow = init_assets()
vec, mat, chunks = init_retriever(kb_text)

# Defaults (simple UI, no technical sidebar controls)
model = "llama-3.1-8b-instant"
temperature = 0.2
top_k = 10

# Top bar with only Clear Chat button
left, right = st.columns([6,1])
with right:
    clear_chat = st.button("Clear chat 🧹", use_container_width=True)

if clear_chat:
    st.session_state.chat = []
    st.success("Chat cleared")

if "chat" not in st.session_state:
    st.session_state.chat = []

def _esc(s: str) -> str:
    return (s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
            .replace("\n","<br>"))

prompt = st.chat_input("Ask about our menu, hours, dietary options, or specials…")
effective_prompt = prompt
if effective_prompt:
    try:
        text, hits = answer(effective_prompt, vec, mat, chunks, patterns, model, temperature, top_k, history=st.session_state.chat)
    except Exception as e:
        text = f"Sorry, I couldn't process that. Please try again. ({e})"
    st.session_state.chat.append(("user", effective_prompt))
    st.session_state.chat.append(("assistant", text))

# Render conversation (user left, assistant right)
for role, content in st.session_state.chat:
    role_cls = "user" if role == "user" else "assistant"
    st.markdown(
        f"""
        <div class="chat-row {role_cls}">
          <div class="bubble {role_cls}">{_esc(content)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.caption("Joni Eats • For allergy concerns or special requests, please speak to our staff.")
