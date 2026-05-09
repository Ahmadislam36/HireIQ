# scorer/ranker.py
# HireIQ — Module 2: Candidate Ranker
# Senior Engineer Note: Ranker = scorer ka output + sorted list.
# Clean separation of concerns — ranker sirf rank karta hai, score nahi.

from scorer.scorer import score_resume


def rank_candidates(resumes: dict, jd_data: dict) -> list:
    """
    Multiple resumes lo → sab score karo → ranked list return karo.

    resumes = {
        "Ali_Khan":   { skills:[...], experience:2, raw_text:"..." },
        "Sara_Ahmed": { skills:[...], experience:4, raw_text:"..." },
    }

    Returns: list of dicts, best candidate pehle
    """
    results = []

    for candidate_name, resume_data in resumes.items():
        scorecard = score_resume(resume_data, jd_data)
        results.append({
            "rank":             0,           # baad mein assign karenge
            "candidate":        candidate_name,
            "final_score":      scorecard["final_score"],
            "grade":            scorecard["grade"],
            "skill_score":      scorecard["skill_score"],
            "keyword_score":    scorecard["keyword_score"],
            "experience_score": scorecard["experience_score"],
            "matched_skills":   scorecard["matched_skills"],
            "missing_skills":   scorecard["missing_skills"],
        })

    # ── Sort by final score descending ──
    results.sort(key=lambda x: x["final_score"], reverse=True)

    # ── Rank assign karo ──
    for i, r in enumerate(results):
        r["rank"] = i + 1

    return results


def print_leaderboard(ranked: list):
    """Terminal mein sundar leaderboard print karo."""
    print("\n" + "=" * 65)
    print("           🏆  HireIQ — CANDIDATE LEADERBOARD  🏆")
    print("=" * 65)
    print(f"{'Rank':<6} {'Candidate':<20} {'Score':>7} {'Grade':<18} {'Matched':>7}")
    print("-" * 65)

    medals = {1: "🥇", 2: "🥈", 3: "🥉"}

    for r in ranked:
        medal = medals.get(r["rank"], "  ")
        print(
            f"{medal} #{r['rank']:<3} "
            f"{r['candidate']:<20} "
            f"{r['final_score']:>6}/100  "
            f"{r['grade']:<18} "
            f"{len(r['matched_skills']):>3} skills"
        )

    print("=" * 65)
    print(f"\n🎯 Top Candidate  : {ranked[0]['candidate']}")
    print(f"   Final Score    : {ranked[0]['final_score']} / 100")
    print(f"   Grade          : {ranked[0]['grade']}")
    print(f"   Matched Skills : {ranked[0]['matched_skills']}")
    print(f"   Missing Skills : {ranked[0]['missing_skills']}")
    print("\n✅ ranker.py working correctly!")


# ── Quick Test ──────────────────────────────────────────────────────────────
if __name__ == "__main__":

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

    sample_resumes = {
        "Ali_Khan": {
            "skills":     ["python", "fastapi", "pandas", "langchain",
                           "rag", "faiss", "numpy", "streamlit"],
            "experience": 2,
            "raw_text":   "2 years exp. Python, FastAPI, LangChain, RAG, FAISS, Pandas, NumPy, Streamlit."
        },
        "Sara_Ahmed": {
            "skills":     ["python", "machine learning", "deep learning",
                           "tensorflow", "scikit-learn", "pandas",
                           "numpy", "nlp", "pytorch"],
            "experience": 4,
            "raw_text":   "4 years exp. Python, ML, Deep Learning, TensorFlow, PyTorch, NLP, scikit-learn."
        },
        "Usman_Malik": {
            "skills":     ["python", "pandas", "numpy", "flask"],
            "experience": 1,
            "raw_text":   "1 year exp. Python, Pandas, NumPy, Flask basics."
        },
        "Ayesha_Raza": {
            "skills":     ["python", "machine learning", "nlp", "langchain",
                           "rag", "faiss", "fastapi", "tensorflow",
                           "pytorch", "scikit-learn", "pandas", "numpy"],
            "experience": 5,
            "raw_text":   "5 years exp. Full ML stack — Python, TensorFlow, PyTorch, NLP, RAG, LangChain, FAISS, FastAPI."
        },
    }

    ranked = rank_candidates(sample_resumes, sample_jd)
    print_leaderboard(ranked)