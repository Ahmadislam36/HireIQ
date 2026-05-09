import re
import spacy

nlp = spacy.load("en_core_web_sm")

SKILLS_LIST = [
    "python", "machine learning", "deep learning", "nlp", "langchain",
    "faiss", "streamlit", "pandas", "numpy", "scikit-learn", "tensorflow",
    "pytorch", "flask", "fastapi", "mongodb", "sql", "docker", "aws",
    "hugging face", "rag", "opencv", "matplotlib", "seaborn", "keras",
    "git", "github", "html", "css", "api"
]

def extract_skills(text):
    text_lower = text.lower()
    found_skills = []
    for skill in SKILLS_LIST:
        if skill in text_lower:
            found_skills.append(skill)
    return list(set(found_skills))

def extract_education(text):
    education = []
    edu_keywords = ["bachelor", "master", "phd", "bs", "ms", "b.s", "m.s",
                    "university", "college", "institute"]
    lines = text.split("\n")
    for line in lines:
        if any(word in line.lower() for word in edu_keywords):
            education.append(line.strip())
    return education

def extract_experience(text):
    experience = []
    exp_keywords = ["intern", "engineer", "developer", "analyst",
                    "manager", "trainee", "consultant", "lead"]
    lines = text.split("\n")
    for line in lines:
        if any(word in line.lower() for word in exp_keywords):
            experience.append(line.strip())
    return experience

def extract_all(text):
    return {
        "skills":     extract_skills(text),
        "education":  extract_education(text),
        "experience": extract_experience(text)
    }

if __name__ == "__main__":
    from pdf_extractor import extract_text_from_pdf
    text = extract_text_from_pdf("data/uploads/Ahmad_Islam.pdf")
    result = extract_all(text)
    print("\n✅ SKILLS:", result["skills"])
    print("\n✅ EDUCATION:", result["education"])
    print("\n✅ EXPERIENCE:", result["experience"])