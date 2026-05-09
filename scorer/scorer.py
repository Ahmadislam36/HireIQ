# scorer/scorer.py
# HireIQ — Module 2: Resume Scorer
# Senior Engineer Note: Weighted scoring = fair + explainable results.
# Recruiter ko pata hona chahiye KYU score itna hai.

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# ── Weights (yahan tune kar sakte ho later) ──────────────────────────────
WEIGHT_SKILLS     = 0.60   # Skill match sabse important
WEIGHT_KEYWORDS   = 0.25   # Context match
WEIGHT_EXPERIENCE = 0.15   # Experience level


def score_skills(resume_skills: list, jd_skills: list) -> tuple:
    """
    Kitni JD skills resume mein hain?
    Returns: (score_0_to_100, matched_skills, missing_skills)
    """
    if not jd_skills:
        return 100.0, [], []

    resume_set = set(s.lower() for s in resume_skills)
    jd_set     = set(s.lower() for s in jd_skills)

    matched = list(resume_set & jd_set)
    missing = list(jd_set - resume_set)
    score   = (len(matched) / len(jd_set)) * 100

    return round(score, 2), matched, missing


def score_keywords(resume_text: str, jd_text: str) -> float:
    """
    TF-IDF + Cosine Similarity se semantic overlap check karo.
    Returns: score 0 to 100
    """
    if not resume_text.strip() or not jd_text.strip():
        return 0.0

    vectorizer = TfidfVectorizer(stop_words='english')
    try:
        tfidf_matrix = vectorizer.fit_transform([resume_text, jd_text])
        similarity   = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
        return round(float(similarity[0][0]) * 100, 2)
    except Exception:
        return 0.0


def score_experience(resume_exp_years, jd_exp_years) -> float:
    if isinstance(resume_exp_years, list): resume_exp_years = resume_exp_years[0] if resume_exp_years else 0
    if isinstance(jd_exp_years, list): jd_exp_years = jd_exp_years[0] if jd_exp_years else 0
    try:
        resume_exp_years = int(float(str(resume_exp_years).strip())) if resume_exp_years else 0
    except:
        resume_exp_years = 0
    try:
        jd_exp_years = int(float(str(jd_exp_years).strip())) if jd_exp_years else 0
    except:
        jd_exp_years = 0
    """
    Experience match karo.
    - JD ne kuch nahi manga → full marks
    - Resume mein zyada hai → full marks
    - Kam hai → proportional score
    Returns: score 0 to 100
    """
    if jd_exp_years == 0:
        return 100.0
    if resume_exp_years >= jd_exp_years:
        return 100.0

    score = (resume_exp_years / jd_exp_years) * 100
    return round(score, 2)


def calculate_final_score(skill_score: float,
                           keyword_score: float,
                           experience_score: float) -> float:
    """Weighted average from all 3 components."""
    final = (
        skill_score     * WEIGHT_SKILLS +
        keyword_score   * WEIGHT_KEYWORDS +
        experience_score * WEIGHT_EXPERIENCE
    )
    return round(final, 2)


def score_resume(resume_data: dict, jd_data: dict) -> dict:
    """
    Main function — ek resume + ek JD lo, full scorecard return karo.

    resume_data keys: skills, experience, raw_text (from Module 1)
    jd_data keys:     skills, experience, raw_text (from jd_parser)
    """
    # ── Calculate each component ──
    skill_score, matched, missing = score_skills(
        resume_data.get("skills", []),
        jd_data.get("skills", [])
    )
    keyword_score = score_keywords(
        resume_data.get("raw_text", ""),
        jd_data.get("raw_text", "")
    )
    exp_score = score_experience(
        resume_data.get("experience", 0),
        jd_data.get("experience", 0)
    )
    final = calculate_final_score(skill_score, keyword_score, exp_score)

    # ── Grade assign karo ──
    if final >= 85:
        grade = "🟢 Excellent"
    elif final >= 70:
        grade = "🔵 Good"
    elif final >= 50:
        grade = "🟡 Average"
    else:
        grade = "🔴 Poor"

    return {
        "final_score":      final,
        "grade":            grade,
        "skill_score":      skill_score,
        "keyword_score":    keyword_score,
        "experience_score": exp_score,
        "matched_skills":   matched,
        "missing_skills":   missing,
    }


# ── Quick Test ──────────────────────────────────────────────────────────────
if __name__ == "__main__":

    # Fake resume data (Module 1 se aata normally)
    sample_resume = {
        "skills":     ["python", "fastapi", "pandas", "langchain",
                       "rag", "faiss", "numpy", "streamlit"],
        "experience": 2,
        "raw_text":   """
            Data Science Intern with 2 years experience.
            Skilled in Python, FastAPI, LangChain, RAG pipelines,
            FAISS vector databases, Pandas, NumPy, and Streamlit.
            Built an end-to-end AI recruitment assistant.
        """
    }

    # Fake JD data (jd_parser se aata normally)
    sample_jd = {
        "skills":     ["python", "machine learning", "deep learning",
                       "tensorflow", "pytorch", "nlp", "rag",
                       "langchain", "fastapi", "faiss",
                       "scikit-learn", "pandas", "numpy"],
        "experience": 3,
        "raw_text":   """
            Machine Learning Engineer — 3+ years experience required.
            Must know Python, TensorFlow, PyTorch, NLP, RAG, LangChain,
            FastAPI, FAISS, scikit-learn, Pandas, NumPy.
        """
    }

    result = score_resume(sample_resume, sample_jd)

    print("\n" + "=" * 50)
    print("       📊 RESUME SCORECARD")
    print("=" * 50)
    print(f"  Final Score     : {result['final_score']} / 100")
    print(f"  Grade           : {result['grade']}")
    print("-" * 50)
    print(f"  Skill Score     : {result['skill_score']} / 100  (60% weight)")
    print(f"  Keyword Score   : {result['keyword_score']} / 100  (25% weight)")
    print(f"  Experience Score: {result['experience_score']} / 100  (15% weight)")
    print("-" * 50)
    print(f"  Matched Skills  : {result['matched_skills']}")
    print(f"  Missing Skills  : {result['missing_skills']}")
    print("=" * 50)
    print("\n✅ scorer.py working correctly!")