import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')))

import plotly.graph_objects as go
from plotly.subplots import make_subplots


def create_ranking_chart(ranked_candidates):
    """Candidates ka bar chart — score ke saath."""
    names = [r["candidate"] for r in ranked_candidates]
    scores = [r["final_score"] for r in ranked_candidates]
    colors = []
    for s in scores:
        if s >= 85:
            colors.append("#2ecc71")
        elif s >= 70:
            colors.append("#3498db")
        elif s >= 50:
            colors.append("#f39c12")
        else:
            colors.append("#e74c3c")

    fig = go.Figure(go.Bar(
        x=names,
        y=scores,
        marker_color=colors,
        text=[f"{s}/100" for s in scores],
        textposition="outside",
    ))
    fig.update_layout(
        title="HireIQ — Candidate Rankings",
        xaxis_title="Candidates",
        yaxis_title="Score",
        yaxis=dict(range=[0, 110]),
        template="plotly_white",
        height=400,
    )
    return fig


def create_score_breakdown_chart(candidate_name, skill_score, keyword_score, exp_score):
    """Ek candidate ka score breakdown — 3 components."""
    fig = go.Figure(go.Bar(
        x=["Skill Match", "Keyword Match", "Experience"],
        y=[skill_score, keyword_score, exp_score],
        marker_color=["#3498db", "#2ecc71", "#f39c12"],
        text=[f"{skill_score}%", f"{keyword_score}%", f"{exp_score}%"],
        textposition="outside",
    ))
    fig.update_layout(
        title=f"Score Breakdown — {candidate_name}",
        yaxis=dict(range=[0, 110]),
        template="plotly_white",
        height=350,
    )
    return fig


def create_skill_gap_chart(matched, missing, candidate_name):
    """Donut chart — matched vs missing skills."""
    fig = go.Figure(go.Pie(
        labels=["Matched Skills", "Missing Skills"],
        values=[len(matched), len(missing)],
        hole=0.55,
        marker_colors=["#2ecc71", "#e74c3c"],
        textinfo="label+percent",
    ))
    fig.update_layout(
        title=f"Skill Gap — {candidate_name}",
        template="plotly_white",
        height=350,
    )
    return fig


def create_comparison_chart(ranked_candidates):
    """Multi-bar chart — skill, keyword, experience scores compare karo."""
    names = [r["candidate"] for r in ranked_candidates]
    skill_scores = [r["skill_score"] for r in ranked_candidates]
    keyword_scores = [r["keyword_score"] for r in ranked_candidates]
    exp_scores = [r["experience_score"] for r in ranked_candidates]

    fig = go.Figure()
    fig.add_trace(go.Bar(name="Skill", x=names, y=skill_scores, marker_color="#3498db"))
    fig.add_trace(go.Bar(name="Keyword", x=names, y=keyword_scores, marker_color="#2ecc71"))
    fig.add_trace(go.Bar(name="Experience", x=names, y=exp_scores, marker_color="#f39c12"))

    fig.update_layout(
        barmode="group",
        title="HireIQ — Score Comparison",
        yaxis_title="Score",
        template="plotly_white",
        height=400,
    )
    return fig


if __name__ == "__main__":
    sample_ranked = [
        {"candidate": "Ayesha_Raza", "final_score": 89, "skill_score": 92, "keyword_score": 85, "experience_score": 100},
        {"candidate": "Sara_Ahmed",  "final_score": 76, "skill_score": 75, "keyword_score": 80, "experience_score": 100},
        {"candidate": "Ali_Khan",    "final_score": 63, "skill_score": 61, "keyword_score": 72, "experience_score": 66},
        {"candidate": "Usman_Malik", "final_score": 28, "skill_score": 23, "keyword_score": 35, "experience_score": 33},
    ]

    print("Creating charts...")
    fig1 = create_ranking_chart(sample_ranked)
    fig1.show()

    fig2 = create_comparison_chart(sample_ranked)
    fig2.show()

    fig3 = create_score_breakdown_chart("Ali_Khan", 61, 72, 66)
    fig3.show()

    fig4 = create_skill_gap_chart(
        matched=["python", "fastapi", "pandas", "langchain"],
        missing=["tensorflow", "pytorch", "nlp", "scikit-learn"],
        candidate_name="Ali_Khan"
    )
    fig4.show()

    print("charts.py working!")