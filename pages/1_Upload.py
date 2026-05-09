import streamlit as st
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from resume_parser.pdf_extractor import extract_text_from_pdf
from resume_parser.skill_extractor import extract_all
from resume_parser.cleaner import clean_text

st.set_page_config(page_title="Upload — HireIQ", page_icon="📤", layout="wide")
st.title("📤 Upload Resumes")
st.markdown("---")

# Job Description
st.subheader("Step 1 — Job Description")
jd_text = st.text_area("Job Description paste karo:", height=200,
    placeholder="We are looking for a Machine Learning Engineer with 3+ years experience...")

if jd_text:
    from scorer.jd_parser import parse_job_description
    jd_data = parse_job_description(jd_text)
    st.session_state["jd_data"] = jd_data
    st.success(f"JD Parsed! Skills found: {len(jd_data['skills'])}")
    with st.expander("JD Skills dekho"):
        st.write(jd_data['skills'])

st.markdown("---")

# Resume Upload
st.subheader("Step 2 — Upload Resumes")
uploaded_files = st.file_uploader(
    "PDF files upload karo",
    type=["pdf"],
    accept_multiple_files=True
)

if uploaded_files:
    resumes = {}
    progress = st.progress(0)

    for i, file in enumerate(uploaded_files):
        save_path = f"data/uploads/{file.name}"
        os.makedirs("data/uploads", exist_ok=True)

        with open(save_path, "wb") as f:
            f.write(file.read())

        raw_text = extract_text_from_pdf(save_path)
        clean = clean_text(raw_text)
        extracted = extract_all(clean)

        name = file.name.replace(".pdf", "")
        resumes[name] = {
            "skills": extracted["skills"],
            "experience": extracted["experience"],
            "education": extracted["education"],
            "raw_text": clean
        }
        progress.progress((i+1) / len(uploaded_files))

    st.session_state["resumes"] = resumes
    st.success(f"{len(resumes)} resumes uploaded successfully!")

    st.markdown("---")
    st.subheader("Uploaded Resumes:")
    for name, data in resumes.items():
        with st.expander(f"📄 {name}"):
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Skills:** {len(data['skills'])} found")
                st.write(data['skills'])
            with col2:
                st.write(f"**Experience:** {data['experience']} years")
                st.write(f"**Education:** {data['education']}")

    if st.button("Results dekhne jao →", type="primary"):
        st.switch_page("pages/2_Results.py")