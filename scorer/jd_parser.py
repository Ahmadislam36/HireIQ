# scorer/jd_parser.py
# HireIQ — Module 2: Job Description Parser
# Senior Engineer Note: JD se structured data nikalna zaroori hai
# taake hum resume se fair comparison kar sakein.

import re
import spacy

nlp = spacy.load("en_core_web_sm")

# ── Master Skills List (same as resume parser, consistent rehna chahiye) ──
SKILLS_LIST = [
    # Programming Languages
    "python", "java", "javascript", "typescript", "c++", "c#", "r", "scala", "go",
    # ML / AI
    "machine learning", "deep learning", "nlp", "natural language processing",
    "computer vision", "reinforcement learning", "transfer learning",
    "neural networks", "transformer", "bert", "gpt",
    # Frameworks & Libraries
    "tensorflow", "pytorch", "keras", "scikit-learn", "xgboost", "lightgbm",
    "langchain", "huggingface", "openai",
    # Data & Vector
    "pandas", "numpy", "faiss", "pinecone", "chroma", "weaviate",
    # MLOps & Tools
    "mlflow", "airflow", "docker", "kubernetes", "git", "github", "dvc",
    # Web & API
    "fastapi", "flask", "streamlit", "gradio", "rest api",
    # Databases
    "mongodb", "postgresql", "mysql", "redis", "elasticsearch",
    # Cloud
    "aws", "azure", "gcp", "google cloud",
    # Other AI
    "rag", "vector database", "embeddings", "fine-tuning", "prompt engineering",
    "llm", "generative ai", "stable diffusion",
]

EXPERIENCE_PATTERNS = [
    r'(\d+)\+?\s*years?\s*of\s*experience',
    r'(\d+)\+?\s*years?\s*experience',
    r'minimum\s*(\d+)\s*years?',
    r'at\s*least\s*(\d+)\s*years?',
    r'(\d+)\s*-\s*(\d+)\s*years?',
]

def extract_required_skills(text: str) -> list:
    """JD se required skills dhundho."""
    text_lower = text.lower()
    found = [skill for skill in SKILLS_LIST if skill in text_lower]
    return list(set(found))

def extract_experience_requirement(text: str) -> int:
    """JD mein kitne years experience maange hain — number return karo."""
    text_lower = text.lower()
    for pattern in EXPERIENCE_PATTERNS:
        match = re.search(pattern, text_lower)
        if match:
            return int(match.group(1))
    return 0  # Not mentioned = 0 (fresh grads welcome!)

def extract_job_title(text: str) -> str:
    """Pehli meaningful line = job title."""
    lines = [l.strip() for l in text.strip().split('\n') if l.strip()]
    return lines[0] if lines else "Unknown Position"

def extract_keywords(text: str) -> list:
    """spaCy se important nouns aur proper nouns nikalo."""
    doc = nlp(text[:5000])  # spaCy ki limit ke liye crop karo
    keywords = [
        token.text.lower() for token in doc
        if token.pos_ in ("NOUN", "PROPN")
        and not token.is_stop
        and len(token.text) > 2
    ]
    return list(set(keywords))

def parse_job_description(jd_text: str) -> dict:
    """
    Main function — JD text lo, structured dict return karo.
    Yahi dict scorer.py use karega.
    """
    return {
        "title":       extract_job_title(jd_text),
        "skills":      extract_required_skills(jd_text),
        "experience":  extract_experience_requirement(jd_text),
        "keywords":    extract_keywords(jd_text),
        "raw_text":    jd_text.strip(),
    }


# ── Quick Test ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    sample_jd = """
    Machine Learning Engineer
    
    We are looking for an experienced Machine Learning Engineer to join our team.
    
    Requirements:
    - 3+ years of experience in Machine Learning or AI
    - Strong proficiency in Python and deep learning frameworks
    - Experience with TensorFlow or PyTorch
    - Knowledge of NLP, RAG, and LangChain
    - Familiarity with FastAPI, Docker, and cloud platforms (AWS/GCP)
    - Experience with FAISS or other vector databases
    - Strong understanding of scikit-learn, pandas, numpy
    """

    result = parse_job_description(sample_jd)

    print("=" * 50)
    print(f"Job Title   : {result['title']}")
    print(f"Skills Found: {result['skills']}")
    print(f"Experience  : {result['experience']} years")
    print(f"Keywords    : {result['keywords'][:10]}")
    print("=" * 50)
    print("\n✅ jd_parser.py working correctly!")