import os
import json
import streamlit as st
from dotenv import load_dotenv
from resume_parser import (
    parse_job_description,
    parse_resume,
    identify_skill_gaps,
    extract_text_from_file
)
from agent import SkillAssessmentAgent
from learning_plan import generate_learning_plan

load_dotenv()

# ─── Page Config ───────────────────────────────────────────
st.set_page_config(
    page_title="AI Skill Assessment Agent",
    page_icon="🤖",
    layout="wide"
)

# ─── Custom CSS ────────────────────────────────────────────
st.markdown("""
<style>
    .main { background-color: #0f172a; }
    .stApp { background-color: #0f172a; color: #e2e8f0; }
    .skill-matched { background:#064e3b; color:#6ee7b7; padding:5px 12px; border-radius:20px; margin:3px; display:inline-block; font-size:0.85rem; }
    .skill-gap-critical { background:#450a0a; color:#fca5a5; padding:5px 12px; border-radius:20px; margin:3px; display:inline-block; font-size:0.85rem; }
    .skill-gap-nice { background:#431407; color:#fed7aa; padding:5px 12px; border-radius:20px; margin:3px; display:inline-block; font-size:0.85rem; }
    .chat-bot { background:#1e3a5f; padding:15px; border-radius:10px; margin:8px 0; border-left:4px solid #3b82f6; }
    .chat-user { background:#4c1d95; padding:15px; border-radius:10px; margin:8px 0; border-left:4px solid #7c3aed; }
    .phase-card { background:#1e293b; padding:20px; border-radius:10px; margin:10px 0; border-left:4px solid #3b82f6; }
    .metric-card { background:#1e293b; padding:20px; border-radius:10px; text-align:center; }
    .stButton>button { background:linear-gradient(135deg,#3b82f6,#7c3aed); color:white; border:none; border-radius:8px; padding:10px 20px; font-weight:600; width:100%; }
    .stButton>button:hover { opacity:0.9; }
    h1,h2,h3 { color:#93c5fd !important; }
    .stTextArea>div>div>textarea { background:#1e293b; color:#e2e8f0; border:1px solid #475569; }
    .stFileUploader { background:#1e293b; border-radius:8px; }
</style>
""", unsafe_allow_html=True)

# ─── Session State Init ────────────────────────────────────
def init_session():
    defaults = {
        "step": 1,
        "jd_data": None,
        "resume_data": None,
        "gaps_data": None,
        "agent": None,
        "chat_history": [],
        "assessment_complete": False,
        "learning_plan": None,
        "assessed_skills": {}
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_session()

# ─── Header ───────────────────────────────────────────────
st.markdown("# 🤖 AI Skill Assessment & Learning Plan Agent")
st.markdown("*A resume tells you what someone claims to know — not how well they actually know it.*")
st.divider()

# ─── Progress Bar ─────────────────────────────────────────
steps = ["📤 Upload", "📊 Analysis", "💬 Assessment", "📚 Learning Plan"]
cols = st.columns(4)
for i, (col, step) in enumerate(zip(cols, steps)):
    with col:
        if st.session_state.step > i + 1:
            st.success(step)
        elif st.session_state.step == i + 1:
            st.info(step)
        else:
            st.markdown(f"<div style='padding:8px;color:#64748b;text-align:center'>{step}</div>", unsafe_allow_html=True)

st.divider()

# ══════════════════════════════════════════════════════════
# STEP 1 — UPLOAD
# ══════════════════════════════════════════════════════════
if st.session_state.step == 1:
    st.markdown("## 📤 Step 1 — Upload Job Description & Resume")
    st.markdown("Paste the texts below or upload your resume file.")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📋 Job Description")
        jd_text = st.text_area(
            "Paste the job description here",
            height=300,
            placeholder="We are looking for a Senior Python Developer...",
            label_visibility="collapsed"
        )

    with col2:
        st.markdown("### 📄 Your Resume")
        resume_text = st.text_area(
            "Paste your resume here",
            height=250,
            placeholder="John Doe - Software Developer...",
            label_visibility="collapsed"
        )
        st.markdown("**or upload a file (PDF / DOCX / TXT)**")
        uploaded_file = st.file_uploader(
            "Upload Resume",
            type=["pdf", "docx", "txt"],
            label_visibility="collapsed"
        )

    if st.button("🚀 Analyze Skills & Start Assessment"):
        if not jd_text.strip():
            st.error("Please enter a Job Description")
        elif not resume_text.strip() and uploaded_file is None:
            st.error("Please enter resume text or upload a file")
        else:
            with st.spinner("🔍 Analyzing JD and Resume with AI..."):
                try:
                    # Handle uploaded file
                    if uploaded_file is not None:
                        os.makedirs("uploads", exist_ok=True)
                        file_path = f"uploads/{uploaded_file.name}"
                        with open(file_path, "wb") as f:
                            f.write(uploaded_file.getbuffer())
                        resume_text = extract_text_from_file(file_path)

                    jd_data = parse_job_description(jd_text)
                    resume_data = parse_resume(resume_text)
                    gaps_data = identify_skill_gaps(jd_data, resume_data)

                    st.session_state.jd_data = jd_data
                    st.session_state.resume_data = resume_data
                    st.session_state.gaps_data = gaps_data
                    st.session_state.step = 2
                    st.rerun()

                except Exception as e:
                    st.error(f"Error: {str(e)}")

# ══════════════════════════════════════════════════════════
# STEP 2 — ANALYSIS
# ══════════════════════════════════════════════════════════
elif st.session_state.step == 2:
    st.markdown("## 📊 Step 2 — Skill Gap Analysis")

    gaps = st.session_state.gaps_data
    jd = st.session_state.jd_data

    st.markdown(f"### Role: **{jd.get('role_title', 'N/A')}** | Level: **{jd.get('seniority', 'N/A')}** | Experience: **{jd.get('experience_years', 'N/A')} years**")
    st.divider()

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Skills Required", gaps['total_required'])
    with col2:
        st.metric("✅ Skills You Have", gaps['match_count'], delta="Matched")
    with col3:
        st.metric("❌ Skills to Learn", gaps['gap_count'], delta=f"-{gaps['gap_count']}", delta_color="inverse")

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### ✅ Matched Skills")
        if gaps['matched_skills']:
            html = "".join([f"<span class='skill-matched'>✅ {s['skill']}</span>" for s in gaps['matched_skills']])
            st.markdown(html, unsafe_allow_html=True)
        else:
            st.warning("No matched skills found")

    with col2:
        st.markdown("### 🔴 Must-Have Gaps")
        critical = [s for s in gaps['skill_gaps'] if s['importance'] == 'must-have']
        if critical:
            html = "".join([f"<span class='skill-gap-critical'>❌ {s['skill']}</span>" for s in critical])
            st.markdown(html, unsafe_allow_html=True)
        else:
            st.success("No critical gaps!")

    with col3:
        st.markdown("### 🟠 Nice-to-Have Gaps")
        nice = [s for s in gaps['skill_gaps'] if s['importance'] == 'nice-to-have']
        if nice:
            html = "".join([f"<span class='skill-gap-nice'>⚠️ {s['skill']}</span>" for s in nice])
            st.markdown(html, unsafe_allow_html=True)
        else:
            st.info("No nice-to-have gaps")

    st.divider()

    if st.button("🎯 Start Conversational Assessment"):
        with st.spinner("Starting assessment..."):
            agent = SkillAssessmentAgent(
                st.session_state.jd_data,
                st.session_state.resume_data,
                st.session_state.gaps_data
            )
            greeting = agent.start_assessment()
            first_q = agent.assess_next_skill()
            st.session_state.agent = agent
            st.session_state.chat_history = [
                {"role": "bot", "content": greeting + "\n\n" + first_q}
            ]
            st.session_state.step = 3
            st.rerun()

# ══════════════════════════════════════════════════════════
# STEP 3 — ASSESSMENT CHAT
# ══════════════════════════════════════════════════════════
elif st.session_state.step == 3:
    st.markdown("## 💬 Step 3 — Conversational Skill Assessment")
    st.markdown("Answer the AI interviewer's questions honestly. It will assess your real proficiency.")
    st.divider()

    # Display chat history
    for msg in st.session_state.chat_history:
        if msg["role"] == "bot":
            st.markdown(f"<div class='chat-bot'>🤖 <strong>AI Interviewer</strong><br><br>{msg['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='chat-user'>👤 <strong>You</strong><br><br>{msg['content']}</div>", unsafe_allow_html=True)

    st.divider()

    if not st.session_state.assessment_complete:
        user_input = st.text_area("Your Answer", placeholder="Type your answer here...", height=100, key=f"input_{len(st.session_state.chat_history)}")

        if st.button("📨 Send Answer"):
            if user_input.strip():
                st.session_state.chat_history.append({"role": "user", "content": user_input})

                with st.spinner("AI is evaluating your answer..."):
                    agent = st.session_state.agent
                    response = agent.process_answer(user_input)
                    st.session_state.agent = agent
                    st.session_state.chat_history.append({"role": "bot", "content": response})
                    st.session_state.assessed_skills = agent.assessed_skills
                    st.session_state.assessment_complete = agent.assessment_complete
                    st.rerun()
    else:
        st.success("✅ Assessment Complete!")
        if st.button("📚 Generate My Personalised Learning Plan"):
            st.session_state.step = 4
            st.rerun()

# ══════════════════════════════════════════════════════════
# STEP 4 — LEARNING PLAN
# ══════════════════════════════════════════════════════════
elif st.session_state.step == 4:
    st.markdown("## 📚 Step 4 — Your Personalised Learning Plan")
    st.divider()

    if st.session_state.learning_plan is None:
        with st.spinner("🧠 Generating your personalised learning plan..."):
            assessment_data = {
                "jd_data": st.session_state.jd_data,
                "resume_data": st.session_state.resume_data,
                "gaps_data": st.session_state.gaps_data,
                "assessed_skills": st.session_state.assessed_skills
            }
            plan = generate_learning_plan(assessment_data)
            st.session_state.learning_plan = plan

    plan = st.session_state.learning_plan

    st.markdown(f"### ⏱️ Total Duration: **{plan.get('total_duration', 'N/A')}**")
    st.divider()

    for phase in plan.get("phases", []):
        with st.expander(f"📌 Phase {phase['phase']}: {phase['title']} — {phase['duration']}", expanded=True):
            st.markdown(f"**🎯 Goal:** {phase['goal']}")
            st.markdown(f"**🛠️ Skills:** {', '.join(phase['skills'])}")
            st.markdown("**📚 Resources:**")
            for r in phase.get("resources", []):
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.markdown(f"🔗 [{r['title']}]({r['url']})")
                with col2:
                    st.markdown(f"⏱️ {r['duration']}")
                with col3:
                    st.markdown(f"🎯 {r['priority']}")

    if plan.get("adjacent_skills"):
        st.divider()
        st.markdown("### 🔗 Adjacent Skills to Explore")
        html = "".join([f"<span class='skill-matched'>{s}</span>" for s in plan['adjacent_skills']])
        st.markdown(html, unsafe_allow_html=True)

    if plan.get("tips"):
        st.divider()
        st.markdown("### 💡 Learning Tips")
        for tip in plan["tips"]:
            st.markdown(f"- {tip}")

    st.divider()
    if st.button("🔄 Start Over with a New Assessment"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()