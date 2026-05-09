import streamlit as st
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

st.set_page_config(page_title="Results — HireIQ", page_icon="🏆", layout="wide")
st.title("🏆 Candidate Rankings")
st.markdown("---")

if "resumes" not in st.session_state or "jd_data" not in st.session_state:
    st.warning("Pehle resumes upload karo!")
    st.stop()

from scorer.ranker import rank_candidates
from dashboard.charts import create_ranking_chart, create_comparison_chart

resumes = st.session_state["resumes"]
jd_data = st.session_state["jd_data"]

with st.spinner("Ranking candidates..."):
    ranked = rank_candidates(resumes, jd_data)
    st.session_state["ranked"] = ranked

medals = {1: "🥇", 2: "🥈", 3: "🥉"}

for r in ranked:
    medal = medals.get(r["rank"], "🎖️")
    with st.container():
        col1, col2, col3, col4, col5 = st.columns([1,3,2,2,2])
        with col1:
            st.markdown(f"## {medal}")
        with col2:
            st.markdown(f"### {r['candidate']}")
            st.caption(r['grade'])
        with col3:
            st.metric("Final Score", f"{r['final_score']}/100")
        with col4:
            st.metric("Skill Match", f"{r['skill_score']}/100")
        with col5:
            st.metric("Experience", f"{r['experience_score']}/100")
        st.markdown("---")

st.subheader("Score Charts")
col1, col2 = st.columns(2)
with col1:
    fig1 = create_ranking_chart(ranked)
    st.plotly_chart(fig1, use_container_width=True)
with col2:
    fig2 = create_comparison_chart(ranked)
    st.plotly_chart(fig2, use_container_width=True)

if st.button("Skill Gap Analysis →", type="primary"):
    st.switch_page("pages/3_Skill_Gap.py")