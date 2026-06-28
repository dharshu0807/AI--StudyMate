import streamlit as st
import time
import random
import base64
from datetime import datetime

# ─── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI StudyMate",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Master CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Google Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

/* ── Root Variables ── */
:root {
  --bg-0:   #05060f;
  --bg-1:   #0f172a;
  --bg-2:   #111827;
  --bg-3:   #1e1b4b;
  --glass:  rgba(255,255,255,0.04);
  --glass2: rgba(255,255,255,0.07);
  --border: rgba(255,255,255,0.08);
  --border2:rgba(255,255,255,0.14);
  --purple: #a855f7;
  --blue:   #3b82f6;
  --cyan:   #06b6d4;
  --pink:   #ec4899;
  --mint:   #10b981;
  --text:   #e2e8f0;
  --muted:  #64748b;
  --card-r: 20px;
}

/* ── Global Reset ── */
*, *::before, *::after { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"],
[data-testid="stApp"] {
  background: linear-gradient(135deg, var(--bg-0) 0%, var(--bg-1) 40%, var(--bg-2) 70%, var(--bg-3) 100%) !important;
  min-height: 100vh;
  font-family: 'DM Sans', sans-serif;
  color: var(--text);
}

/* Animated mesh background */
[data-testid="stAppViewContainer"]::before {
  content: '';
  position: fixed;
  inset: 0;
  background:
    radial-gradient(ellipse 80% 60% at 20% 10%, rgba(168,85,247,0.12) 0%, transparent 60%),
    radial-gradient(ellipse 60% 50% at 80% 80%, rgba(59,130,246,0.10) 0%, transparent 60%),
    radial-gradient(ellipse 50% 40% at 50% 50%, rgba(6,182,212,0.06) 0%, transparent 60%);
  pointer-events: none;
  z-index: 0;
}

/* Floating orbs */
[data-testid="stAppViewContainer"]::after {
  content: '';
  position: fixed;
  width: 600px; height: 600px;
  top: -200px; right: -200px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(168,85,247,0.07) 0%, transparent 70%);
  pointer-events: none;
  z-index: 0;
  animation: orb-drift 18s ease-in-out infinite alternate;
}

@keyframes orb-drift {
  from { transform: translate(0,0) scale(1);   }
  to   { transform: translate(-80px,60px) scale(1.15); }
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
  background: rgba(10,10,20,0.72) !important;
  backdrop-filter: blur(24px) !important;
  border-right: 1px solid var(--border2) !important;
  padding: 0 !important;
}
[data-testid="stSidebar"] > div:first-child { padding-top: 0 !important; }

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header,
[data-testid="stToolbar"],
[data-testid="stDecoration"] { display: none !important; }
           

/* ── Scrollbars ── */
::-webkit-scrollbar { width: 4px; }
           

/* ── Scrollbars ── */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb {
  background: linear-gradient(var(--purple), var(--blue));
  border-radius: 4px;
}

/* ── Block container ── */
.block-container {
  padding: 0 2rem 2rem 2rem !important;
  max-width: 100% !important;
}

/* ── Glass Card Base ── */
.glass-card {
  background: var(--glass);
  border: 1px solid var(--border);
  border-radius: var(--card-r);
  backdrop-filter: blur(16px);
  transition: border-color .3s, box-shadow .3s, transform .25s;
}
.glass-card:hover {
  border-color: var(--border2);
  box-shadow: 0 8px 40px rgba(168,85,247,0.12);
  transform: translateY(-2px);
}

/* ── Hero Header ── */
.hero-wrap {
  text-align: center;
  padding: 2.4rem 1rem 1.2rem;
  position: relative;
}
.hero-badge {
  display: inline-flex;
  align-items: center;
  gap: .5rem;
  background: linear-gradient(135deg,rgba(168,85,247,.15),rgba(59,130,246,.15));
  border: 1px solid rgba(168,85,247,.35);
  border-radius: 999px;
  padding: .35rem 1.1rem;
  font-size: .75rem;
  font-family: 'DM Sans', sans-serif;
  font-weight: 500;
  letter-spacing: .08em;
  text-transform: uppercase;
  color: var(--purple);
  margin-bottom: 1rem;
}
.hero-title {
  font-family: 'Syne', sans-serif;
  font-size: clamp(2.4rem, 5vw, 3.6rem);
  font-weight: 800;
  line-height: 1.05;
  background: linear-gradient(135deg, #e2e8f0 10%, var(--purple) 45%, var(--cyan) 80%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin: 0 0 .5rem;
}

.hero-sub {
  font-size: 1.05rem;
  color: var(--muted);
  font-weight: 300;
  letter-spacing: .01em;
  margin: 0 0 1.4rem;
}
.hero-divider {
  width: 100%;
  height: 1px;
  background: linear-gradient(90deg, transparent, var(--purple), var(--cyan), transparent);
  opacity: .35;
  margin-bottom: 1.6rem;
}

/* ── Sidebar Profile ── */
.profile-ring {
  width: 68px; height: 68px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--purple), var(--cyan));
  padding: 2px;
  margin: 0 auto 1rem;
}
.profile-inner {
  width: 100%; height: 100%;
  border-radius: 50%;
  background: var(--bg-1);
  display: flex; align-items: center; justify-content: center;
  font-size: 1.6rem;
}
.profile-name {
  font-family: 'Syne', sans-serif;
  font-size: 1rem;
  font-weight: 700;
  text-align: center;
  color: var(--text);
}
.profile-tag {
  font-size: .75rem;
  color: var(--cyan);
  text-align: center;
  margin-bottom: 1.4rem;
}
.stat-row {
  display: flex;
  gap: .6rem;
  margin: 0 1rem 1.4rem;
}
.stat-pill {
  flex: 1;
  background: var(--glass2);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: .6rem .4rem;
  text-align: center;
}
.stat-num {
  font-family: 'Syne', sans-serif;
  font-size: 1.1rem;
  font-weight: 700;
  background: linear-gradient(135deg, var(--purple), var(--blue));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
.stat-lbl { font-size: .65rem; color: var(--muted); }

/* ── Sidebar nav label ── */
.nav-label {
  font-size: .65rem;
  font-weight: 600;
  letter-spacing: .12em;
  text-transform: uppercase;
  color: var(--muted);
  padding: .5rem 1.2rem .4rem;
}

/* ── Chat History Items ── */
.history-item {
  display: flex;
  align-items: center;
  gap: .7rem;
  padding: .65rem 1.2rem;
  border-radius: 12px;
  margin: .2rem .6rem;
  cursor: pointer;
  transition: background .2s, border-color .2s;
  border: 1px solid transparent;
}
.history-item:hover {
  background: var(--glass2);
  border-color: var(--border);
}
.history-item.active {
  background: linear-gradient(135deg,rgba(168,85,247,.18),rgba(59,130,246,.12));
  border-color: rgba(168,85,247,.35);
}
.history-icon { font-size: 1rem; }
.history-text { flex: 1; }
.history-title { font-size: .82rem; color: var(--text); font-weight: 500; }
.history-time  { font-size: .68rem; color: var(--muted); }

/* ── Tool Cards ── */
.tools-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: .7rem;
  margin: 0 .5rem 1.4rem;
}
.tool-card {
  background: var(--glass);
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: .8rem .5rem;
  text-align: center;
  cursor: pointer;
  transition: all .25s;
}
.tool-card:hover {
  background: var(--glass2);
  border-color: rgba(168,85,247,.4);
  box-shadow: 0 4px 24px rgba(168,85,247,.15);
  transform: translateY(-2px);
}
.tool-icon { font-size: 1.4rem; margin-bottom: .35rem; }
.tool-name { font-size: .68rem; font-weight: 500; color: var(--text); }

/* ── Message Bubbles ── */
.msg-row {
  display: flex;
  gap: .9rem;
  margin-bottom: 1.2rem;
  animation: msg-in .35s ease both;
}
@keyframes msg-in {
  from { opacity:0; transform:translateY(12px); }
  to   { opacity:1; transform:translateY(0);    }
}
.msg-row.user { flex-direction: row-reverse; }

.avatar {
  width: 34px; height: 34px;
  border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-size: .95rem;
  flex-shrink: 0;
  margin-top: .15rem;
}
.avatar.ai {
  background: linear-gradient(135deg, var(--purple), var(--blue));
  box-shadow: 0 0 14px rgba(168,85,247,.45);
}
.avatar.user {
  background: linear-gradient(135deg, var(--blue), var(--cyan));
  box-shadow: 0 0 14px rgba(59,130,246,.35);
}

.bubble {
  max-width: 72%;
  padding: .9rem 1.2rem;
  border-radius: 18px;
  line-height: 1.65;
  font-size: .9rem;
}
.bubble.ai {
  background: linear-gradient(135deg,rgba(168,85,247,.12),rgba(59,130,246,.08));
  border: 1px solid rgba(168,85,247,.22);
  border-top-left-radius: 4px;
  color: var(--text);
}
.bubble.user {
  background: linear-gradient(135deg,rgba(59,130,246,.22),rgba(6,182,212,.15));
  border: 1px solid rgba(6,182,212,.28);
  border-top-right-radius: 4px;
  color: var(--text);
}
.bubble-meta {
  font-size: .65rem;
  color: var(--muted);
  margin-top: .45rem;
}

/* ── Typing Indicator ── */
.typing-wrap {
  display: flex; gap: .9rem; align-items: flex-end; margin-bottom: 1rem;
}
.typing-bubble {
  background: linear-gradient(135deg,rgba(168,85,247,.12),rgba(59,130,246,.08));
  border: 1px solid rgba(168,85,247,.22);
  border-radius: 18px; border-top-left-radius: 4px;
  padding: .85rem 1.1rem;
  display: flex; gap: .35rem; align-items: center;
}
.dot {
  width: 7px; height: 7px;
  border-radius: 50%;
  background: var(--purple);
  animation: bounce .9s ease-in-out infinite;
}
.dot:nth-child(2) { animation-delay: .18s; background: var(--blue);  }
.dot:nth-child(3) { animation-delay: .36s; background: var(--cyan);  }
@keyframes bounce {
  0%,80%,100% { transform: translateY(0);   opacity:.5; }
  40%          { transform: translateY(-8px); opacity:1;  }
}

/* ── Chat Container ── */
.chat-box {
  background: var(--glass);
  border: 1px solid var(--border2);
  border-radius: var(--card-r);
  padding: 1.4rem 1.4rem .4rem;
  min-height: 420px;
  max-height: 520px;
  overflow-y: auto;
  backdrop-filter: blur(12px);
  margin-bottom: 1rem;
}

/* Button overrides */
.stButton > button {
  border-radius: 12px !important;
  font-family: 'DM Sans', sans-serif !important;
  font-weight: 500 !important;
  transition: all .25s !important;
  border: none !important;
}
.stButton > button[kind="primary"] {
  background: linear-gradient(135deg, var(--purple), var(--blue)) !important;
  color: white !important;
  box-shadow: 0 0 18px rgba(168,85,247,.4) !important;
}
.stButton > button[kind="primary"]:hover {
  box-shadow: 0 0 28px rgba(168,85,247,.65) !important;
  transform: translateY(-1px) !important;
}
.stButton > button[kind="secondary"] {
  background: var(--glass2) !important;
  color: var(--text) !important;
  border: 1px solid var(--border2) !important;
}
.stButton > button[kind="secondary"]:hover {
  border-color: rgba(168,85,247,.4) !important;
  background: rgba(168,85,247,.1) !important;
}

/* File uploader */
[data-testid="stFileUploadDropzone"] {
  background: var(--glass) !important;
  border: 1px dashed var(--border2) !important;
  border-radius: 14px !important;
  color: var(--muted) !important;
}
[data-testid="stFileUploadDropzone"]:hover {
  border-color: rgba(168,85,247,.45) !important;
  background: rgba(168,85,247,.05) !important;
}

/* Selectbox */
[data-testid="stSelectbox"] select,
[data-testid="stSelectbox"] > div > div {
  background: var(--glass) !important;
  border: 1px solid var(--border2) !important;
  border-radius: 12px !important;
  color: var(--text) !important;
  font-family: 'DM Sans', sans-serif !important;
}

/* Toggle & slider */
[data-testid="stToggle"] label { color: var(--text) !important; }

/* Info box */
.stAlert {
  background: var(--glass) !important;
  border: 1px solid rgba(6,182,212,.3) !important;
  border-radius: 12px !important;
  color: var(--text) !important;
}

/* Spinner */
[data-testid="stSpinner"] > div { border-top-color: var(--purple) !important; }
            /* ── Chat Input Dark Fix ── */
[data-testid="stChatInput"] {
  background: rgba(15, 23, 42, 0.85) !important;
  border: 1px solid rgba(168, 85, 247, 0.35) !important;
  border-radius: 16px !important;
  backdrop-filter: blur(12px) !important;
}
[data-testid="stChatInput"] textarea {
  background: transparent !important;
  color: #e2e8f0 !important;
  font-family: 'DM Sans', sans-serif !important;
  caret-color: #a855f7 !important;
}
[data-testid="stChatInput"] textarea::placeholder {
  color: #64748b !important;
}
[data-testid="stChatInput"] button {
  background: linear-gradient(135deg, #a855f7, #3b82f6) !important;
  border-radius: 10px !important;
}
/* Fix white background leak around chat input */
[data-testid="stBottom"] {
  background: linear-gradient(to top, #05060f, transparent) !important;
  border-top: 1px solid rgba(255,255,255,0.06) !important;
}
[data-testid="stBottom"] > div {
  background: transparent !important;
}

/* ── Section headers ── */
.section-label {
  font-size: .68rem;
  font-weight: 600;
  letter-spacing: .12em;
  text-transform: uppercase;
  color: var(--muted);
  margin: 1.1rem 0 .6rem;
}

/* ── Neon divider ── */
.neon-divider {
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(168,85,247,.4), rgba(6,182,212,.4), transparent);
  margin: .8rem 0;
}

/* ── Tag pills ── */
.tag-row { display:flex; flex-wrap:wrap; gap:.4rem; margin:.5rem 0; }
.tag {
  padding:.25rem .75rem;
  border-radius:999px;
  font-size:.7rem;
  font-weight:500;
  border:1px solid;
}
.tag-purple { background:rgba(168,85,247,.12); border-color:rgba(168,85,247,.35); color:var(--purple); }
.tag-cyan   { background:rgba(6,182,212,.12);  border-color:rgba(6,182,212,.35);  color:var(--cyan);   }
.tag-pink   { background:rgba(236,72,153,.12); border-color:rgba(236,72,153,.35); color:var(--pink);   }
.tag-blue   { background:rgba(59,130,246,.12); border-color:rgba(59,130,246,.35); color:var(--blue);   }

/* ── Welcome card ── */
.welcome-card {
  background: linear-gradient(135deg,rgba(168,85,247,.08),rgba(59,130,246,.06));
  border: 1px solid rgba(168,85,247,.2);
  border-radius: 18px;
  padding: 1.4rem 1.6rem;
  margin-bottom: 1.2rem;
  text-align: center;
}
.welcome-icon { font-size: 2.4rem; margin-bottom: .5rem; }
.welcome-title {
  font-family: 'Syne', sans-serif;
  font-size: 1.15rem;
  font-weight: 700;
  color: var(--text);
  margin-bottom: .35rem;
}
.welcome-desc { font-size: .83rem; color: var(--muted); line-height: 1.5; }

/* ── Quick prompt chips ── */
.chips-row { display:flex; flex-wrap:wrap; gap:.5rem; margin-bottom:1.2rem; justify-content:center; }
.chip {
  padding:.4rem .9rem;
  border-radius:999px;
  background:var(--glass2);
  border:1px solid var(--border2);
  font-size:.76rem;
  font-weight:500;
  color:var(--text);
  cursor:pointer;
  transition:all .2s;
}
.chip:hover {
  background:rgba(168,85,247,.15);
  border-color:rgba(168,85,247,.4);
  box-shadow:0 0 12px rgba(168,85,247,.2);
}

/* ── Mode indicator ── */
.mode-pill {
  display:inline-flex;
  align-items:center;
  gap:.45rem;
  background:linear-gradient(135deg,rgba(236,72,153,.15),rgba(168,85,247,.15));
  border:1px solid rgba(236,72,153,.35);
  border-radius:999px;
  padding:.35rem 1rem;
  font-size:.74rem;
  font-weight:600;
  color:var(--pink);
  margin-bottom:1rem;
  animation:pulse-glow 2.5s ease-in-out infinite;
}
@keyframes pulse-glow {
  0%,100% { box-shadow:0 0 0 0 rgba(236,72,153,0); }
  50%      { box-shadow:0 0 14px 2px rgba(236,72,153,.25); }
}

</style>
""", unsafe_allow_html=True)

# ─── Session State ───────────────────────────────────────────────────────────────
def init_state():
    defaults = {
        "messages": [],
        "chat_history": [
            {"title": "Calculus Integration Tips", "time": "2h ago",  "icon": "∫"},
            {"title": "Quantum Physics Notes",      "time": "5h ago",  "icon": "⚛"},
            {"title": "Essay Outline – History",    "time": "Yesterday","icon": "📜"},
            {"title": "Python OOP Concepts",        "time": "2d ago",  "icon": "🐍"},
        ],
        "active_chat": 0,
        "typing": False,
        "exam_mode": False,
        "total_queries": 47,
        "streak_days": 12,
        "uploaded_file": None,
        "active_tool": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ─── AI Response Generator ───────────────────────────────────────────────────────
def get_ai_response(user_msg, tool=None):
    """Calls the completely free live Gemini model based on the selected tool or chat input."""
    import google.generativeai as genai
    
    GEMINI_API_KEY = st.secrets["AQ.Ab8RN6KBdGtF7Ev0KmKIhhgYA0iqBrXVq_BRZwbTawncXahTdA"]
    
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        
        system_instructions = {
            "notes": "You are an expert academic tutor. Take the user's topic and generate highly organized, structured revision notes with bullet points and key definitions.",
            "quiz": "You are a professor. Create a highly accurate 5-question multiple-choice quiz based on the user's request. Mark the correct answer clearly with a checkmark (✓).",
            "summary": "You are an advanced reading assistant. Provide a high-quality, comprehensive summary of the text provided, emphasizing critical takeaways.",
            "explain": "You are a master communicator. Explain the requested concept in incredibly simple terms, using an intuitive real-world analogy.",
            "flashcards": "Generate a list of 5 interactive study flashcards showing a clear 'Front' question and 'Back' answer layout.",
            "exam": "Act as an academic coach. Analyze the user's topic and outline the top 5 highest-yield areas most likely to show up on a final exam.",
        }
        
        selected_instruction = system_instructions.get(tool, "You are a supportive, genius-level AI study assistant called AI StudyMate.")
        full_prompt = f"System Context: {selected_instruction}\n\nUser Prompt: {user_msg if user_msg else 'Provide an overview of this tool module.'}"
        
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content(full_prompt)
        return response.text
        
    except Exception as e:
        return f"⚠️ Connection Error: (Details: {str(e)})"

def add_message(role, content):
    st.session_state.messages.append({
        "role": role,
        "content": content,
        "time": datetime.now().strftime("%I:%M %p"),
    })

def render_messages():
    if not st.session_state.messages:
        st.markdown("""
        <div class="welcome-card">
          <div class="welcome-icon">✦</div>
          <div class="welcome-title">Welcome to AI StudyMate</div>
          <div class="welcome-desc">
            Your intelligent learning companion — ask questions, generate notes,<br>
            create quizzes, or upload study materials to get started.
          </div>
        </div>
        <div class="chips-row">
          <span class="chip">📐 Explain a concept</span>
          <span class="chip">📝 Generate notes</span>
          <span class="chip">🎯 Create a quiz</span>
          <span class="chip">📄 Summarize PDF</span>
          <span class="chip">🃏 Flashcards</span>
          <span class="chip">🎓 Exam prep</span>
        </div>
        """, unsafe_allow_html=True)
        return

    html = '<div class="chat-box">'
    for msg in st.session_state.messages:
        role_cls = msg["role"]
        av = "✦" if role_cls == "ai" else "👤"
        html += f"""
        <div class="msg-row {role_cls}">
          <div class="avatar {role_cls}">{av}</div>
          <div>
            <div class="bubble {role_cls}">{msg["content"]}</div>
            <div class="bubble-meta">{msg["time"]}</div>
          </div>
        </div>"""
    if st.session_state.typing:
        html += """
        <div class="typing-wrap">
          <div class="avatar ai">✦</div>
          <div class="typing-bubble">
            <div class="dot"></div><div class="dot"></div><div class="dot"></div>
          </div>
        </div>"""
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)


# ─── SIDEBAR ─────────────────────────────────────────────────────────────────────
with st.sidebar:
    # Profile
    st.markdown("""
    <div style="padding:1.4rem 0 .4rem;">
      <div class="profile-ring"><div class="profile-inner">🎓</div></div>
      <div class="profile-name">Dharshu</div>
      <div class="profile-tag">CS &amp; Business Systems · SRM EEC</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="stat-row">
      <div class="stat-pill">
        <div class="stat-num">{st.session_state.total_queries}</div>
        <div class="stat-lbl">Queries</div>
      </div>
      <div class="stat-pill">
        <div class="stat-num">{st.session_state.streak_days}</div>
        <div class="stat-lbl">Day streak</div>
      </div>
      <div class="stat-pill">
        <div class="stat-num">A+</div>
        <div class="stat-lbl">Grade</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="neon-divider"></div>', unsafe_allow_html=True)

    # New Chat / Clear
    c1, c2 = st.columns(2)
    with c1:
        if st.button("✦ New Chat", key="new_chat", use_container_width=True, type="primary"):
            st.session_state.messages = []
            st.session_state.active_tool = None
            st.rerun()
    with c2:
        if st.button("⌫ Clear", key="clear_chat", use_container_width=True, type="secondary"):
            st.session_state.messages = []
            st.rerun()

    st.markdown('<div class="nav-label" style="margin-top:.8rem;">Search Chats</div>', unsafe_allow_html=True)
    search_query = st.text_input(
        "Search chats",
        placeholder="Search your study topics...",
        label_visibility="collapsed",
        key="history_search",
    )

    st.markdown('<div class="nav-label">Chat History</div>', unsafe_allow_html=True)

    normalized_query = search_query.strip().lower()
    has_matching_history = False
    for i, chat in enumerate(st.session_state.chat_history):
        if normalized_query and normalized_query not in chat["title"].lower():
            continue

        has_matching_history = True
        active = "active" if i == st.session_state.active_chat else ""
        if st.button(
            f"{chat['icon']}  {chat['title'][:22]}{'…' if len(chat['title'])>22 else ''}",
            key=f"hist_{i}",
            use_container_width=True,
            type="secondary",
        ):
            st.session_state.active_chat = i

    if normalized_query and not has_matching_history:
        st.caption("No matching chats found.")

    st.markdown('<div class="neon-divider" style="margin-top:.8rem;"></div>', unsafe_allow_html=True)

    # Study tools
    st.markdown('<div class="nav-label">Study Tools</div>', unsafe_allow_html=True)

    TOOLS = [
        ("📝", "Notes",      "notes"),
        ("🎯", "Quiz",       "quiz"),
        ("📄", "Summarize",  "summary"),
        ("💡", "Explain",    "explain"),
        ("🃏", "Flashcards", "flashcards"),
        ("🎓", "Exam Prep",  "exam"),
    ]
    
    cols = st.columns(3)
    for idx, (icon, name, key) in enumerate(TOOLS):
        with cols[idx % 3]:
            if st.button(f"{icon}\n{name}", key=f"tool_{key}", use_container_width=True, type="secondary"):
                st.session_state.active_tool = key
                prompts = {
                    "notes":      "Generate structured study notes on the current topic.",
                    "quiz":       "Create a 5-question quiz to test my understanding.",
                    "summary":    "Summarize the uploaded or recent study material.",
                    "explain":    "Explain the core concept in simple terms with examples.",
                    "flashcards": "Generate a set of revision flashcards.",
                    "exam":       "Activate exam preparation mode and show high-yield topics.",
                }
                add_message("user", prompts[key])
                st.session_state.typing = True
                st.session_state.total_queries += 1
                st.rerun()

    st.markdown('<div class="neon-divider"></div>', unsafe_allow_html=True)

    # Exam mode toggle
    exam_mode = st.toggle("🎓 Exam Mode", value=st.session_state.exam_mode, key="exam_toggle")
    if exam_mode != st.session_state.exam_mode:
        st.session_state.exam_mode = exam_mode
        st.rerun()

    # File upload
    st.markdown('<div class="nav-label" style="margin-top:.4rem;">Upload Materials</div>', unsafe_allow_html=True)
    uploaded = st.file_uploader(
        "Drop PDF or Image",
        type=["pdf", "png", "jpg", "jpeg"],
        label_visibility="collapsed",
        key="file_uploader",
    )
    if uploaded:
        st.session_state.uploaded_file = uploaded.name
        st.success(f"✓ {uploaded.name[:28]}", icon="📎")

    # Subject tags
    st.markdown('<div class="nav-label" style="margin-top:.6rem;">Subjects</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="tag-row" style="padding:0 .1rem;">
      <span class="tag tag-purple">Mathematics</span>
      <span class="tag tag-cyan">Physics</span>
      <span class="tag tag-blue">CS Theory</span>
      <span class="tag tag-pink">DSA</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)


# ─── MAIN AREA ───────────────────────────────────────────────────────────────────

# Hero
st.markdown("""
<div class="hero-wrap">
  <div class="hero-badge">✦ &nbsp;Powered by Generative AI</div>
  <div class="hero-title">AI StudyMate</div>
  <div class="hero-sub">Your Smart Learning Companion</div>
  <div class="hero-divider"></div>
</div>
""", unsafe_allow_html=True)

# Exam mode banner
if st.session_state.exam_mode:
    st.markdown("""
    <div style="display:flex;justify-content:center;margin-bottom:1rem;">
      <div class="mode-pill">🎓 &nbsp;Exam Preparation Mode Active</div>
    </div>
    """, unsafe_allow_html=True)

# Active tool indicator
if st.session_state.active_tool:
    tool_labels = {
        "notes":"Generate Notes","quiz":"Create Quiz","summary":"Summarize PDF",
        "explain":"Explain Concept","flashcards":"Flashcards","exam":"Exam Prep",
    }
    st.markdown(f"""
    <div style="display:flex;justify-content:center;margin-bottom:.8rem;">
      <div class="mode-pill" style="background:linear-gradient(135deg,rgba(168,85,247,.15),rgba(59,130,246,.12));border-color:rgba(168,85,247,.4);color:var(--purple);">
        ✦ &nbsp;Active Tool: {tool_labels.get(st.session_state.active_tool,'')}
      </div>
    </div>
    """, unsafe_allow_html=True)

# Messages
render_messages()

st.markdown("<div style='height:.5rem'></div>", unsafe_allow_html=True)

# ── Input Row (🟩 REPLACED WITH NATIVE VISIBLE CHAT INPUT) ──
user_input = st.chat_input("Ask anything about your studies...")

if user_input:
    add_message("user", user_input.strip())
    st.session_state.typing = True
    st.rerun()

# ── Action buttons row (🎤 Voice input deleted, clean layout) ──
ca, cb, cc = st.columns(3)
with ca:
    pdf_click = st.button("📄 Upload PDF", key="pdf_btn", type="secondary", use_container_width=True)
with cb:
    img_click = st.button("🖼 Upload Image", key="img_btn", type="secondary", use_container_width=True)
with cc:
    clear_tool = st.button("✕ Clear Active Tool", key="tool_clear", type="secondary", use_container_width=True)

if clear_tool:
    st.session_state.active_tool = None
    st.rerun()

if pdf_click or img_click:
    st.info("📎 Use the Upload Materials panel in the sidebar to attach PDF or image files.", icon="📁")

# Simulate AI reply after typing flag
if st.session_state.typing:
    time.sleep(1.4)
    last_user = next(
        (m["content"] for m in reversed(st.session_state.messages) if m["role"] == "user"),
        ""
    )
    # 🟩 FIX: Passes the currently active tool from the sidebar to the API
    current_tool = st.session_state.get("active_tool")
    add_message("ai", get_ai_response(last_user, tool=current_tool))
    st.session_state.typing = False
    st.session_state.total_queries += 1
    
    if len(st.session_state.messages) == 2:
        preview = last_user[:32] + ("…" if len(last_user) > 32 else "")
        st.session_state.chat_history.insert(0, {
            "title": preview,
            "time":  "Just now",
            "icon":  "💬",
        })
    st.rerun()

# ── Footer ──
st.markdown("""
<div style="text-align:center;margin-top:2.5rem;padding-top:1.2rem;
     border-top:1px solid rgba(255,255,255,0.05); pointer-events: none;">
  <span style="font-size:.72rem;color:#334155;letter-spacing:.06em;">
    AI STUDYMATE &nbsp;·&nbsp; BUILT FOR SERIOUS LEARNERS &nbsp;·&nbsp;
    <span style="background:linear-gradient(135deg,#a855f7,#06b6d4);
                 -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                 background-clip:text;">✦ POWERED BY AI</span>
  </span>
</div>
""", unsafe_allow_html=True)
