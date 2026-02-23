# app.py (UI v2: responsive, clean, readable, clutter-free)
import os
from dotenv import load_dotenv

import streamlit as st
import matplotlib.pyplot as plt
from wordcloud import WordCloud

from ai_engine import generate_knowledge_content
from pdf_generator import generate_pdf
from utils import parse_ai_response, show_error

load_dotenv()

# ---------------------------
# Page config (ONLY ONCE)
# ---------------------------
st.set_page_config(
    page_title="AI Knowledge Coach",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------
# UI: clean theme overrides
# ---------------------------
st.markdown("""
<style>
/* Force the 'Topic' label to be black */
div[data-testid="stTextInput"] label {
  color: #0F172A !important;
  font-weight: 700 !important;
  font-size: 1.08rem !important;
}
/* ===========================
   DESIGN TOKENS
=========================== */
:root{
  --bg1:#F8FAFC;
  --bg2:#EEF2FF;
  --card:#FFFFFF;
  --text:#0F172A;
  --muted:#64748B;
  --border:rgba(148,163,184,0.45);
  --shadow:0 12px 28px rgba(15,23,42,0.08);
  --primary:#4F46E5;
  --accent:#F59E0B;
  --radius:18px;
  --radius-sm:14px;
}

/* Force light color-scheme */
:root, .stApp { color-scheme: light !important; }

/* ===========================
   BACKGROUND + LAYOUT
=========================== */
.stApp{
  background:
    radial-gradient(1100px 520px at 12% 0%, rgba(79,70,229,0.14), transparent 60%),
    radial-gradient(900px 520px at 92% 10%, rgba(245,158,11,0.10), transparent 55%),
    linear-gradient(180deg, var(--bg1) 0%, var(--bg2) 55%, var(--bg1) 100%) !important;
  color: var(--text) !important;
}

.block-container{
  max-width: 1180px;
  padding-top: 1.2rem;
  padding-bottom: 2.5rem;
}

header[data-testid="stHeader"]{ background: transparent !important; }

/* ===========================
   SIDEBAR
=========================== */
section[data-testid="stSidebar"]{
  background: rgba(255,255,255,0.90) !important;
  border-right: 1px solid var(--border) !important;
}
section[data-testid="stSidebar"] *{ color: var(--text) !important; }

/* ===========================
   TEXT INPUT
=========================== */
div[data-testid="stTextInput"] input{
  background: var(--card) !important;
  color: var(--text) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius-sm) !important;
  padding: .7rem .9rem !important;
  box-shadow: var(--shadow) !important;
}
div[data-testid="stTextInput"] input::placeholder{ color:#94A3B8 !important; }

/* ===========================
   SELECTBOX — STREAMLIT + BASEWEB FIX
   (THIS fixes the black Summary length / Quiz difficulty)
=========================== */

/* Streamlit wrapper (sometimes works) */
div[data-testid="stSelectbox"] div[role="combobox"]{
  background: var(--card) !important;
  color: var(--text) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius-sm) !important;
  box-shadow: var(--shadow) !important;
}
div[data-testid="stSelectbox"] div[role="combobox"] *{
  color: var(--text) !important;
}

/* BaseWeb select control (most reliable) */
div[data-testid="stSelectbox"] [data-baseweb="select"] > div{
  background: var(--card) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius-sm) !important;
  box-shadow: var(--shadow) !important;
}
div[data-testid="stSelectbox"] [data-baseweb="select"] *{
  color: var(--text) !important;
}

/* The actual input area inside BaseWeb */
div[data-testid="stSelectbox"] [data-baseweb="select"] input{
  color: var(--text) !important;
  background: transparent !important;
}

/* Dropdown menu (portal) */
div[data-baseweb="menu"],
div[data-baseweb="menu"] *{
  background: var(--card) !important;
  color: var(--text) !important;
}
div[data-baseweb="popover"],
div[data-baseweb="popover"] *{
  background: var(--card) !important;
  color: var(--text) !important;
}

/* Menu items hover */
div[data-baseweb="menu"] li:hover,
div[data-baseweb="menu"] li:hover *{
  background: rgba(79,70,229,0.08) !important;
}

/* Extra fallback for listbox portals */
div[role="listbox"], div[role="listbox"] *{
  background: var(--card) !important;
  color: var(--text) !important;
}

/* ===========================
   BUTTONS
=========================== */
div.stButton > button{
  background: linear-gradient(90deg, var(--primary) 0%, #7C3AED 55%, var(--accent) 120%) !important;
  color: #FFFFFF !important;
  border: none !important;
  border-radius: var(--radius-sm) !important;
  padding: .65rem 1.05rem !important;
  font-weight: 800 !important;
  box-shadow: 0 16px 34px rgba(79,70,229,0.22) !important;
}
div.stButton > button:hover{
  transform: translateY(-1px);
  filter: brightness(1.03);
}

/* Form Submit Button (quiz) */
div[data-testid="stFormSubmitButton"] > button{
  background: linear-gradient(90deg, var(--primary) 0%, #7C3AED 55%, var(--accent) 120%) !important;
  color: #FFFFFF !important;
  border: none !important;
  border-radius: var(--radius-sm) !important;
  padding: .65rem 1.05rem !important;
  font-weight: 800 !important;
  box-shadow: 0 16px 34px rgba(79,70,229,0.22) !important;
}

/* Download button */
div.stDownloadButton > button{
  background: #0F172A !important;
  color: #FFFFFF !important;
  border-radius: var(--radius-sm) !important;
  border: none !important;
  padding: .65rem 1.05rem !important;
  font-weight: 800 !important;
}

/* ===========================
   RADIO (Quiz options readable)
=========================== */
div[data-testid="stRadio"]{
  background: rgba(255,255,255,0.95) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius-sm) !important;
  padding: .6rem .8rem !important;
}
div[data-testid="stRadio"] label,
div[data-testid="stRadio"] label *{
  color: var(--text) !important;
  font-weight: 500 !important;
}

/* ===========================
   CARDS
=========================== */
.card{
  background: rgba(255,255,255,0.95);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 1.05rem;
  box-shadow: var(--shadow);
}
.card h3{
  margin-bottom: .6rem;
  font-size: 1.08rem;
  color: var(--text);
}
.card p, .card li{
  color: var(--text);
  font-size: 1rem;
  line-height: 1.55;
}
.muted{ color: var(--muted); }

/* ===========================
   FOOTER
=========================== */
.footer{
  text-align: center;
  color: var(--muted);
  font-size: .9rem;
  margin-top: 2rem;
}
.footer a{
  color: var(--primary);
  text-decoration: none;
}
.footer a:hover{ text-decoration: underline; }

</style>
""", unsafe_allow_html=True)

# ---------------------------
# Helpers
# ---------------------------
def get_azure_config():
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT", "")
    api_key = os.getenv("AZURE_OPENAI_KEY", "")
    deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4.1")
    api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-12-01-preview")
    return endpoint, api_key, deployment, api_version


def reset_app_state():
    keys = [
        "knowledge_data",
        "knowledge_topic",
        "quiz_selected",
        "quiz_submitted",
        "pdf_bytes",
        "topic_value",
    ]
    for k in keys:
        if k in st.session_state:
            del st.session_state[k]


def safe_wordcloud(text: str):
    if not text.strip():
        return None
    wc = WordCloud(width=1100, height=500, background_color="white").generate(text)
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.imshow(wc, interpolation="bilinear")
    ax.axis("off")
    return fig


def card_html(title: str, body_html: str, subtitle: str | None = None):
    sub = f"<div class='muted' style='margin-top:-.35rem;margin-bottom:.65rem;'>{subtitle}</div>" if subtitle else ""
    return f"""
    <div class="card">
      <h3>{title}</h3>
      {sub}
      {body_html}
    </div>
    """


# ---------------------------
# Sidebar (simple + useful)
# ---------------------------
with st.sidebar:
    st.markdown("### Settings")
    st.caption("Tune output and regenerate anytime.")

    temperature = st.slider("Creativity (temperature)", 0.0, 1.0, 0.2, 0.05)
    summary_length = st.selectbox("Summary length", ["Short (60 words)", "Medium (120 words)", "Long (200 words)"])
    quiz_difficulty = st.selectbox("Quiz difficulty", ["Easy", "Medium", "Hard"])

    st.write("")
    st.markdown("<span class='badge'>⚡ Built using GitHub Copilot</span>", unsafe_allow_html=True)

    with st.expander("About Copilot usage"):
        st.write(
            "- Scaffolded modular files\n"
            "- Suggested UI layout + CSS fixes\n"
            "- Improved prompting + JSON parsing\n"
            "- Assisted with PDF export + error handling"
        )

    st.write("")
    st.markdown("---")
    if st.button("Reset / Clear results", use_container_width=True):
        reset_app_state()
        st.rerun()


# ---------------------------
# Header
# ---------------------------
st.markdown(
    """
<div>
  <div class="h-title">AI Knowledge Coach</div>
  <div class="h-sub">Enter a topic → get a structured summary, key insights, interview questions, and a mini quiz.</div>
</div>
""",
    unsafe_allow_html=True,
)

st.write("")

# ---------------------------
# Input Panel (clean + compact)
# ---------------------------
top_left, top_right = st.columns([1.35, 0.65], vertical_alignment="bottom")

with top_left:
    topic = st.text_input(
        
        "Topic",
        value=st.session_state.get("topic_value", "Generative AI"),
        placeholder="e.g., Zero Trust, RAG, Prompt Engineering, Data Modeling…",
    )

with top_right:
    generate_clicked = st.button("✨ Generate", use_container_width=True)

# Lightweight feature strip (no clutter)
st.write("")
f1, f2, f3 = st.columns(3)
with f1:
    st.markdown(card_html("✅ Summary", "<p class='muted'>Short, medium, or long — your choice.</p>"), unsafe_allow_html=True)
with f2:
    st.markdown(card_html("💡 Insights", "<p class='muted'>5 practical takeaways you can apply.</p>"), unsafe_allow_html=True)
with f3:
    st.markdown(card_html("📝 Quiz", "<p class='muted'>5 MCQs + scoring + review.</p>"), unsafe_allow_html=True)

st.write("")

# ---------------------------
# Generate
# ---------------------------
if generate_clicked:
    st.session_state["topic_value"] = topic
    endpoint, api_key, deployment, api_version = get_azure_config()

    if not topic.strip():
        st.warning("Please enter a topic.")
    elif not api_key or not endpoint or not deployment or not api_version:
        st.warning(
            "Azure OpenAI credentials missing. Set: AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_KEY, "
            "AZURE_OPENAI_DEPLOYMENT, AZURE_OPENAI_API_VERSION."
        )
    else:
        with st.spinner("Generating content..."):
            try:
                ai_response = generate_knowledge_content(
                    topic=topic,
                    endpoint=endpoint,
                    api_key=api_key,
                    deployment=deployment,
                    api_version=api_version,
                    temperature=temperature,
                    summary_length=summary_length,
                    quiz_difficulty=quiz_difficulty,
                )

                data = parse_ai_response(ai_response)

                st.session_state["knowledge_data"] = data
                st.session_state["knowledge_topic"] = topic
                st.session_state["quiz_selected"] = {}
                st.session_state["quiz_submitted"] = False
                st.session_state.pop("pdf_bytes", None)

            except Exception as e:
                show_error(e)
                st.stop()

# ---------------------------
# Results
# ---------------------------
if "knowledge_data" in st.session_state:
    data = st.session_state["knowledge_data"]
    current_topic = st.session_state.get("knowledge_topic", topic)

    st.markdown(
        f"<div class='muted' style='margin-bottom:.35rem;'>Results for: <b>{current_topic}</b></div>",
        unsafe_allow_html=True,
    )

    # Summary + Insights + Snapshot + Questions
    left, right = st.columns([1.05, 0.95], vertical_alignment="top")

    with left:
        summary = (data.get("summary") or "").strip()
        st.markdown(
            card_html("Structured Summary", f"<p>{summary}</p>"),
            unsafe_allow_html=True,
        )
        st.write("")

        insights = data.get("insights", []) or []
        insights_html = "".join([f"<li>{i}</li>" for i in insights]) if insights else "<li>No insights returned.</li>"
        st.markdown(
            card_html("Key Insights (5)", f"<ul>{insights_html}</ul>"),
            unsafe_allow_html=True,
        )

    with right:
        # Snapshot (use native container so pyplot/caption behave correctly)
        with st.container(border=True):
            st.subheader("Concept Snapshot", anchor=False)
            st.caption("Word cloud generated from the key insights.")
            insights_text = " ".join(insights).strip()
            fig = safe_wordcloud(insights_text) if insights_text else None
            if fig is not None:
                st.pyplot(fig, use_container_width=True)
            else:
                st.info("No insights yet — generate content to see the snapshot.")

        st.write("")

        qs = data.get("interview_questions", []) or []
        qs_html = "".join([f"<li>{q}</li>" for q in qs]) if qs else "<li>No questions returned.</li>"
        st.markdown(
            card_html("Interview Questions (3)", f"<ol>{qs_html}</ol>"),
            unsafe_allow_html=True,
        )

    st.write("")

    # ---------------------------
    # Quiz (native widgets for stability + readability)
    # ---------------------------
    quiz = data.get("quiz", []) or []

    with st.container(border=True):
        st.subheader("Knowledge Check Quiz (5 MCQs)", anchor=False)
        st.caption("Answer all questions, then submit once. Review answers after submission.")

        if not quiz:
            st.info("No quiz returned by the model.")
        else:
            selected_map = st.session_state.get("quiz_selected", {})
            total = len(quiz)

            # Progress indicator (answered count)
            answered = 0
            for idx in range(1, total + 1):
                if idx in selected_map:
                    answered += 1
            st.progress(min(answered / total, 1.0))
            st.caption(f"Progress: {answered}/{total} answered")

            with st.form("quiz_form", clear_on_submit=False):
                for i, q in enumerate(quiz, start=1):
                    question = q.get("question", "")
                    options = q.get("options", []) or []
                    default_index = selected_map.get(i, 0)

                    st.markdown(f"<div class='quiz-q'>Q{i}. {question}</div>", unsafe_allow_html=True)

                    if options:
                        choice = st.radio(
                            label=f"q{i}",
                            options=options,
                            index=min(default_index, len(options) - 1),
                            key=f"q_{i}_radio",
                            label_visibility="collapsed",
                        )
                        selected_map[i] = options.index(choice)
                    else:
                        st.warning("No options returned for this question.")

                    st.write("")

                submit_quiz = st.form_submit_button("Submit Quiz")

            st.session_state["quiz_selected"] = selected_map

            cols = st.columns([1, 1], vertical_alignment="center")
            with cols[0]:
                if submit_quiz:
                    st.session_state["quiz_submitted"] = True
            with cols[1]:
                st.caption("Tip: Use Reset in sidebar to start fresh anytime.")

            if st.session_state.get("quiz_submitted"):
                score = 0
                for i, q in enumerate(quiz, start=1):
                    options = q.get("options", []) or []
                    answer = q.get("answer", "")
                    picked_idx = selected_map.get(i, 0)
                    picked = options[picked_idx] if options and picked_idx < len(options) else None
                    if picked == answer:
                        score += 1

                st.success(f"Your Score: {score} / {total}")

                with st.expander("Review answers"):
                    for i, q in enumerate(quiz, start=1):
                        options = q.get("options", []) or []
                        answer = q.get("answer", "")
                        picked_idx = selected_map.get(i, 0)
                        picked = options[picked_idx] if options and picked_idx < len(options) else None

                        st.write(f"**Q{i}. {q.get('question', '')}**")
                        if picked == answer:
                            st.success(f"✅ Your answer: {picked}")
                        else:
                            st.error(f"❌ Your answer: {picked}")
                            st.info(f"✔ Correct: {answer}")
                        st.write("")

    st.write("")

    # ---------------------------
    # Export (simple flow)
    # ---------------------------
    exp_l, exp_r = st.columns([1, 1], vertical_alignment="top")

    with exp_l:
        st.markdown(
            card_html(
                "Export as PDF",
                "<p class='muted'>Includes summary, insights, interview questions, and the quiz.</p>",
            ),
            unsafe_allow_html=True,
        )
        st.write("")

        if st.button("📄 Generate PDF", use_container_width=True):
            try:
                st.session_state["pdf_bytes"] = generate_pdf(data, current_topic)
            except Exception as e:
                show_error(e)

        if st.session_state.get("pdf_bytes"):
            st.download_button(
                label="⬇️ Download PDF",
                data=st.session_state["pdf_bytes"],
                file_name=f"{current_topic}_knowledge_coach.pdf",
                mime="application/pdf",
                use_container_width=True,
            )

# Footer
st.markdown(
    '''
<div class="footer">
  AI Knowledge Coach &copy; 2026 — Built for Microsoft Agents League (Creative Apps) <br/>
  <a href="https://github.com/features/copilot" target="_blank">Powered by GitHub Copilot</a>
</div>
''',
    unsafe_allow_html=True,
)