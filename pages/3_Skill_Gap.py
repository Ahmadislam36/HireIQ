import streamlit as st
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

st.set_page_config(page_title="Skill Gap — HireIQ", page_icon="📊", layout="wide")
st.title("📊 Skill Gap Analysis")
st.markdown("---")

if "ranked" not in st.session_state:
    st.warning("Pehle results dekho!")
    st.stop()

from skill_gap.gap_analyzer import analyze_gap, create_gap_chart

ranked = st.session_state["ranked"]
resumes = st.session_state["resumes"]
jd_data = st.session_state["jd_data"]

selected = st.selectbox("Candidate select karo:", [r["candidate"] for r in ranked])

if selected:
    resume = resumes[selected]
    gap = analyze_gap(resume["skills"], jd_data["skills"])
    st.session_state[f"gap_{selected}"] = gap

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Match Score", f"{gap['match_percentage']}%")
    with col2:
        st.metric("Matched Skills", gap['total_matched'])
    with col3:
        st.metric("Missing Skills", gap['total_missing'])

    fig = create_gap_chart(gap, selected)
    st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Matched Skills")
        for s in gap["matched_skills"]:
            st.success(f"✅ {s}")
    with col2:
        st.subheader("Missing Skills")
        for item in gap["missing_details"]:
            icon = {"Beginner":"🟢","Intermediate":"🟡","Advanced":"🔴"}.get(item["difficulty"],"⚪")
            st.error(f"{icon} {item['skill']} — [{item['difficulty']}]")
            st.caption(f"Learn: {item['resource']}")

if st.button("Interview Questions →", type="primary"):
    st.switch_page("pages/4_Interview.py")