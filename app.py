import streamlit as st

st.set_page_config(
    page_title="HireIQ",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🎯 HireIQ — AI Powered Recruitment Assistant")
st.markdown("---")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Modules", "6", "Complete")
with col2:
    st.metric("AI Model", "Gemini", "Active")
with col3:
    st.metric("Features", "5", "Ready")
with col4:
    st.metric("Status", "Live", "")

st.markdown("---")
st.markdown("""
### How to use HireIQ:
1. **Upload** — Resume PDFs upload karo
2. **Results** — Rankings aur scores dekho
3. **Skill Gap** — Missing skills analyze karo
4. **Interview** — AI generated questions
5. **Export** — PDF report download karo
""")

st.info("Left sidebar se koi bhi page select karo!")