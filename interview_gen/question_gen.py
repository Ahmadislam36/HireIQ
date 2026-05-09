import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')))

from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '.env'))

import requests
import json


api_key = "AIzaSyCcoNSzSk33dSxuKDzquC9569LCB-zgQMA"
URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"



def ask_gemini(prompt):
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(URL, headers=headers, json=payload)
    data = response.json()
    if "candidates" not in data:
        error = data.get("error", {})
        msg = error.get("message", str(data))
        raise Exception(f"API Error: {msg}")
    return data["candidates"][0]["content"]["parts"][0]["text"]


def generate_interview(candidate_name, matched_skills, missing_skills, experience=0):
    prompt = f"""
You are an expert technical interviewer for AI/ML roles.

Candidate: {candidate_name}
Experience: {experience} years
Strong Skills: {', '.join(matched_skills) if matched_skills else 'None'}
Weak Skills: {', '.join(missing_skills) if missing_skills else 'None'}

Generate exactly 10 interview questions:
- 5 questions on STRONG skills
- 5 questions on WEAK skills

Format:
STRENGTH QUESTIONS:
1. question
2. question
3. question
4. question
5. question

WEAKNESS QUESTIONS:
1. question
2. question
3. question
4. question
5. question
"""
    print(f"Generating questions for {candidate_name}...")
    raw = ask_gemini(prompt)

    strength_qs = []
    weakness_qs = []
    current = None

    for line in raw.split('\n'):
        line = line.strip()
        if 'STRENGTH' in line.upper():
            current = 'strength'
        elif 'WEAKNESS' in line.upper():
            current = 'weakness'
        elif line and line[0].isdigit() and '.' in line:
            q = line.split('.', 1)[1].strip()
            if current == 'strength':
                strength_qs.append(q)
            elif current == 'weakness':
                weakness_qs.append(q)

    return {
        "candidate": candidate_name,
        "strength_questions": strength_qs,
        "weakness_questions": weakness_qs,
        "total": len(strength_qs) + len(weakness_qs)
    }


def print_interview(result):
    print("\n" + "="*60)
    print(f"   INTERVIEW — {result['candidate'].upper()}")
    print("="*60)
    print("\n  STRENGTH QUESTIONS:")
    print("-"*60)
    for i, q in enumerate(result["strength_questions"], 1):
        print(f"  {i}. {q}")
    print("\n  WEAKNESS QUESTIONS:")
    print("-"*60)
    for i, q in enumerate(result["weakness_questions"], 1):
        print(f"  {i}. {q}")
    print("\n" + "="*60)
    print(f"  Total: {result['total']} questions")
    print("="*60)
    print("\nquestion_gen.py working!")


if __name__ == "__main__":
    result = generate_interview(
        candidate_name="Ali_Khan",
        matched_skills=["python", "fastapi", "langchain", "rag", "faiss", "pandas"],
        missing_skills=["machine learning", "deep learning", "tensorflow", "pytorch"],
        experience=2
    )
    print_interview(result)