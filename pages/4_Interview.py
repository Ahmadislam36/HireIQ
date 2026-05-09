import streamlit as st
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

st.set_page_config(page_title="Interview — HireIQ", page_icon="🤖", layout="wide")
st.title("🤖 AI Interview Questions")
st.markdown("---")

if "ranked" not in st.session_state:
    st.warning("Pehle results dekho!")
    st.stop()

from interview_gen.question_gen import generate_interview

ranked = st.session_state["ranked"]
resumes = st.session_state["resumes"]

selected = st.selectbox("Candidate select karo:", [r["candidate"] for r in ranked])

if selected and st.button("Generate Questions", type="primary"):
    resume = resumes[selected]
    scorecard = next(r for r in ranked if r["candidate"] == selected)

    with st.spinner("Gemini se questions generate ho rahe hain..."):
        result = generate_interview(
            candidate_name=selected,
            matched_skills=scorecard["matched_skills"],
            missing_skills=scorecard["missing_skills"],
            experience=resume.get("experience", 0)
        )
        st.session_state[f"questions_{selected}"] = result

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Strength Based Questions")
        for i, q in enumerate(result["strength_questions"], 1):
            st.info(f"**Q{i}.** {q}")
    with col2:
        st.subheader("Weakness Based Questions")
        for i, q in enumerate(result["weakness_questions"], 1):
            st.warning(f"**Q{i}.** {q}")

if st.button("Export PDF →", type="primary"):
    st.switch_page("pages/5_Export.py")