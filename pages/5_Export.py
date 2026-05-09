import streamlit as st
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

st.set_page_config(page_title="Export — HireIQ", page_icon="📥", layout="wide")
st.title("📥 Export PDF Reports")
st.markdown("---")

if "ranked" not in st.session_state:
    st.warning("Pehle sab steps complete karo!")
    st.stop()

from dashboard.report import generate_report
from skill_gap.gap_analyzer import analyze_gap

ranked = st.session_state["ranked"]
resumes = st.session_state["resumes"]
jd_data = st.session_state["jd_data"]

selected = st.selectbox("Candidate select karo:", [r["candidate"] for r in ranked])

if selected and st.button("PDF Generate Karo", type="primary"):
    scorecard = next(r for r in ranked if r["candidate"] == selected)
    resume = resumes[selected]
    gap = analyze_gap(resume["skills"], jd_data["skills"])
    questions = st.session_state.get(f"questions_{selected}", {
        "strength_questions": ["Question not generated yet"],
        "weakness_questions": ["Question not generated yet"]
    })

    with st.spinner("PDF ban raha hai..."):
        path = generate_report(selected, scorecard, gap, questions)

    with open(path, "rb") as f:
        st.download_button(
            label="PDF Download Karo",
            data=f,
            file_name=f"{selected}_HireIQ_Report.pdf",
            mime="application/pdf"
        )
    st.success("PDF ready hai!")