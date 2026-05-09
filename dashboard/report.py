import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')))

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.enums import TA_CENTER, TA_LEFT


def generate_report(candidate_name, scorecard, gap_data, questions, output_path=None):
    """Complete candidate report PDF generate karo."""

    if not output_path:
        os.makedirs("data/reports", exist_ok=True)
        output_path = f"data/reports/{candidate_name}_report.pdf"

    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=2*cm, leftMargin=2*cm,
        topMargin=2*cm, bottomMargin=2*cm
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('T', parent=styles['Title'],
        fontSize=20, textColor=colors.HexColor('#1a1a2e'),
        spaceAfter=6, alignment=TA_CENTER)
    sub_style = ParagraphStyle('S', parent=styles['Normal'],
        fontSize=10, textColor=colors.HexColor('#4a4a8a'),
        spaceAfter=12, alignment=TA_CENTER)
    section_style = ParagraphStyle('Sec', parent=styles['Heading1'],
        fontSize=12, textColor=colors.white,
        backColor=colors.HexColor('#1a1a2e'),
        borderPadding=(5,8,5,8), spaceAfter=8, spaceBefore=12)
    body_style = ParagraphStyle('B', parent=styles['Normal'],
        fontSize=10, spaceAfter=4, leftIndent=10)

    story = []

    # Header
    story.append(Paragraph("HireIQ", title_style))
    story.append(Paragraph(f"Candidate Report — {candidate_name}", sub_style))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#1a1a2e')))
    story.append(Spacer(1, 0.3*cm))

    # Score Summary
    story.append(Paragraph("  SCORE SUMMARY", section_style))
    score_data = [
        ["Metric", "Score"],
        ["Final Score", f"{scorecard.get('final_score', 0)} / 100"],
        ["Grade", scorecard.get('grade', 'N/A')],
        ["Skill Score", f"{scorecard.get('skill_score', 0)} / 100"],
        ["Keyword Score", f"{scorecard.get('keyword_score', 0)} / 100"],
        ["Experience Score", f"{scorecard.get('experience_score', 0)} / 100"],
    ]
    t = Table(score_data, colWidths=[9*cm, 7*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1a1a2e')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 10),
        ('BACKGROUND', (0,1), (-1,1), colors.HexColor('#e8f5e9')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cccccc')),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t)
    story.append(Spacer(1, 0.3*cm))

    # Skill Gap
    story.append(Paragraph("  SKILL GAP ANALYSIS", section_style))
    matched = gap_data.get('matched_skills', [])
    missing = gap_data.get('missing_skills', [])
    story.append(Paragraph(f"Match Score: {gap_data.get('match_percentage', 0)}%", body_style))
    story.append(Paragraph(f"Matched Skills: {', '.join(matched) if matched else 'None'}", body_style))
    story.append(Paragraph(f"Missing Skills: {', '.join(missing) if missing else 'None'}", body_style))
    story.append(Spacer(1, 0.3*cm))

    # Interview Questions
    story.append(Paragraph("  INTERVIEW QUESTIONS", section_style))
    story.append(Paragraph("Strength Based:", ParagraphStyle('SB', parent=styles['Normal'],
        fontSize=11, fontName='Helvetica-Bold', spaceAfter=4, leftIndent=10)))
    for i, q in enumerate(questions.get('strength_questions', []), 1):
        story.append(Paragraph(f"{i}. {q}", body_style))

    story.append(Spacer(1, 0.2*cm))
    story.append(Paragraph("Weakness Based:", ParagraphStyle('WB', parent=styles['Normal'],
        fontSize=11, fontName='Helvetica-Bold', spaceAfter=4, leftIndent=10)))
    for i, q in enumerate(questions.get('weakness_questions', []), 1):
        story.append(Paragraph(f"{i}. {q}", body_style))

    story.append(Spacer(1, 0.3*cm))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#cccccc')))
    story.append(Paragraph(
        "HireIQ — AI Powered Recruitment Assistant",
        ParagraphStyle('F', parent=styles['Normal'], fontSize=8,
                      textColor=colors.HexColor('#888888'), alignment=TA_CENTER)))

    doc.build(story)
    print(f"Report saved: {output_path}")
    return output_path


if __name__ == "__main__":
    sample_scorecard = {
        "final_score": 63, "grade": "Good",
        "skill_score": 61, "keyword_score": 72, "experience_score": 66,
    }
    sample_gap = {
        "match_percentage": 61.5,
        "matched_skills": ["python", "fastapi", "pandas", "langchain", "rag"],
        "missing_skills": ["tensorflow", "pytorch", "nlp", "scikit-learn"],
    }
    sample_questions = {
        "strength_questions": [
            "How do you optimize a RAG pipeline?",
            "Explain FAISS index types.",
            "How does LangChain memory work?",
            "FastAPI async vs sync endpoints?",
            "Pandas performance optimization tips?",
        ],
        "weakness_questions": [
            "What is backpropagation?",
            "Difference between CNN and RNN?",
            "How would you start learning TensorFlow?",
            "What is transfer learning?",
            "Explain NLP tokenization.",
        ],
    }

    path = generate_report("Ali_Khan", sample_scorecard, sample_gap, sample_questions)
    print(f"PDF created: {path}")
    print("report.py working!")