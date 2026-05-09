import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')))

import plotly.graph_objects as go
from plotly.subplots import make_subplots

LEARNING_RESOURCES = {
    "python":           "https://docs.python.org/3/tutorial/",
    "machine learning": "https://www.coursera.org/learn/machine-learning",
    "deep learning":    "https://www.coursera.org/specializations/deep-learning",
    "nlp":              "https://huggingface.co/learn/nlp-course",
    "langchain":        "https://python.langchain.com/docs/get_started",
    "faiss":            "https://faiss.ai/",
    "tensorflow":       "https://www.tensorflow.org/tutorials",
    "pytorch":          "https://pytorch.org/tutorials/",
    "scikit-learn":     "https://scikit-learn.org/stable/tutorial/",
    "fastapi":          "https://fastapi.tiangolo.com/tutorial/",
    "streamlit":        "https://docs.streamlit.io/",
    "docker":           "https://docs.docker.com/get-started/",
    "rag":              "https://python.langchain.com/docs/use_cases/question_answering/",
    "pandas":           "https://pandas.pydata.org/docs/getting_started/",
    "numpy":            "https://numpy.org/learn/",
}

SKILL_DIFFICULTY = {
    "python": "Beginner", "pandas": "Beginner", "numpy": "Beginner",
    "streamlit": "Beginner", "flask": "Beginner",
    "scikit-learn": "Intermediate", "fastapi": "Intermediate",
    "machine learning": "Intermediate", "nlp": "Intermediate",
    "langchain": "Intermediate", "faiss": "Intermediate",
    "docker": "Intermediate", "rag": "Intermediate",
    "tensorflow": "Advanced", "pytorch": "Advanced",
    "deep learning": "Advanced",
}


def analyze_gap(resume_skills, jd_skills):
    resume_set = set(s.lower() for s in resume_skills)
    jd_set     = set(s.lower() for s in jd_skills)

    matched = sorted(list(resume_set & jd_set))
    missing = sorted(list(jd_set - resume_set))
    extra   = sorted(list(resume_set - jd_set))

    match_pct = round(len(matched) / len(jd_set) * 100, 1) if jd_set else 100.0

    missing_details = []
    for skill in missing:
        missing_details.append({
            "skill":      skill,
            "difficulty": SKILL_DIFFICULTY.get(skill, "Intermediate"),
            "resource":   LEARNING_RESOURCES.get(skill, "https://www.google.com/search?q=learn+" + skill.replace(" ", "+")),
        })

    order = {"Beginner": 0, "Intermediate": 1, "Advanced": 2}
    missing_details.sort(key=lambda x: order.get(x["difficulty"], 1))

    return {
        "matched_skills":   matched,
        "missing_skills":   missing,
        "extra_skills":     extra,
        "missing_details":  missing_details,
        "match_percentage": match_pct,
        "total_jd_skills":  len(jd_set),
        "total_matched":    len(matched),
        "total_missing":    len(missing),
    }


def create_gap_chart(gap_data, candidate_name="Candidate"):
    fig = make_subplots(
        rows=1, cols=2,
        specs=[[{"type": "pie"}, {"type": "bar"}]],
        subplot_titles=[
            f"{candidate_name} — Skill Match",
            "Missing Skills by Difficulty"
        ]
    )

    fig.add_trace(
        go.Pie(
            labels=["Matched", "Missing"],
            values=[gap_data["total_matched"], gap_data["total_missing"]],
            hole=0.55,
            marker_colors=["#2ecc71", "#e74c3c"],
            textinfo="label+percent",
        ),
        row=1, col=1
    )

    difficulty_counts = {"Beginner": 0, "Intermediate": 0, "Advanced": 0}
    for item in gap_data["missing_details"]:
        difficulty_counts[item["difficulty"]] += 1

    fig.add_trace(
        go.Bar(
            x=list(difficulty_counts.keys()),
            y=list(difficulty_counts.values()),
            marker_color=["#2ecc71", "#f39c12", "#e74c3c"],
            text=list(difficulty_counts.values()),
            textposition="outside",
        ),
        row=1, col=2
    )

    fig.update_layout(
        title_text="HireIQ — Skill Gap Analysis",
        title_font_size=20,
        showlegend=False,
        height=450,
        template="plotly_white",
    )

    return fig


def print_gap_report(gap_data, candidate_name="Candidate"):
    print("\n" + "=" * 60)
    print(f"   SKILL GAP REPORT — {candidate_name.upper()}")
    print("=" * 60)
    print(f"   Match Score    : {gap_data['match_percentage']}%")
    print(f"   Total Required : {gap_data['total_jd_skills']} skills")
    print(f"   You Have       : {gap_data['total_matched']} skills")
    print(f"   You Need       : {gap_data['total_missing']} skills")
    print("-" * 60)

    print("\n  MATCHED SKILLS:")
    print(f"     {', '.join(gap_data['matched_skills']) if gap_data['matched_skills'] else 'None'}")

    print("\n  MISSING SKILLS (Seekhne ka order):")
    for item in gap_data["missing_details"]:
        icon = {"Beginner": "G", "Intermediate": "Y", "Advanced": "R"}.get(item["difficulty"], "-")
        print(f"     [{icon}] {item['skill']:<25} [{item['difficulty']}]")
        print(f"           Learn: {item['resource']}")

    if gap_data["extra_skills"]:
        print(f"\n  BONUS SKILLS:")
        print(f"     {', '.join(gap_data['extra_skills'])}")

    print("\n" + "=" * 60)
    print("  gap_analyzer.py working correctly!")


if __name__ == "__main__":
    resume_skills = [
        "python", "fastapi", "pandas", "langchain",
        "rag", "faiss", "numpy", "streamlit"
    ]
    jd_skills = [
        "python", "machine learning", "deep learning",
        "tensorflow", "pytorch", "nlp", "rag",
        "langchain", "fastapi", "faiss",
        "scikit-learn", "pandas", "numpy"
    ]

    gap = analyze_gap(resume_skills, jd_skills)
    print_gap_report(gap, candidate_name="Ali_Khan")

    fig = create_gap_chart(gap, candidate_name="Ali_Khan")
    fig.show()