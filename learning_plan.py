import os
import json
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

import streamlit as st

def get_api_key():
    try:
        return st.secrets["GROQ_API_KEY"]
    except:
        return os.getenv("GROQ_API_KEY", "").strip()

client = Groq(api_key=get_api_key())

def generate_learning_plan(assessment_data):
    """Generate a personalised learning plan based on assessment results."""

    jd_data = assessment_data.get("jd_data", {})
    resume_data = assessment_data.get("resume_data", {})
    gaps_data = assessment_data.get("gaps_data", {})
    assessed_skills = assessment_data.get("assessed_skills", {})

    role = jd_data.get("role_title", "the target role")
    skill_gaps = gaps_data.get("skill_gaps", [])
    matched_skills = gaps_data.get("matched_skills", [])

    proficiency_summary = []
    for skill, data in assessed_skills.items():
        proficiency_summary.append(f"{skill}: {data.get('proficiency', 'Unknown')}")

    prompt = f"""You are an expert learning coach. Based on the following candidate assessment, create a detailed personalised learning plan.

Role Target: {role}
Candidate Current Skills: {', '.join(resume_data.get('technical_skills', []))}
Assessed Proficiency: {', '.join(proficiency_summary) if proficiency_summary else 'Not assessed yet'}
Skill Gaps (Missing Skills): {', '.join([g['skill'] for g in skill_gaps])}
Must-Have Gaps: {', '.join([g['skill'] for g in skill_gaps if g['importance'] == 'must-have'])}
Nice-to-Have Gaps: {', '.join([g['skill'] for g in skill_gaps if g['importance'] == 'nice-to-have'])}

Create a learning plan in this EXACT JSON format with no extra text:
{{
  "total_duration": "X weeks",
  "phases": [
    {{
      "phase": 1,
      "title": "Foundation",
      "duration": "2 weeks",
      "skills": ["skill1", "skill2"],
      "resources": [
        {{
          "skill": "skill1",
          "type": "Course",
          "title": "Course name",
          "url": "https://...",
          "duration": "10 hours",
          "priority": "High"
        }}
      ],
      "goal": "What the candidate will achieve in this phase"
    }}
  ],
  "adjacent_skills": ["skill1", "skill2"],
  "tips": ["tip1", "tip2"]
}}

Focus on:
1. Skills the candidate can realistically learn given their existing background
2. Real, specific resources (Udemy, freeCodeCamp, official docs, YouTube)
3. Logical learning order (adjacent skills first)
4. Time estimates per skill
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}]
    )

    raw = response.choices[0].message.content.strip()
    raw = raw.replace("```json", "").replace("```", "").strip()

    try:
        return json.loads(raw)
    except Exception:
        start = raw.find("{")
        end = raw.rfind("}") + 1
        if start != -1 and end != 0:
            return json.loads(raw[start:end])
        return {"error": "Could not parse learning plan", "raw": raw}


def format_learning_plan(plan):
    """Format learning plan as readable text."""
    if "error" in plan:
        return f"Error generating plan: {plan['error']}"

    output = []
    output.append(f"PERSONALISED LEARNING PLAN")
    output.append(f"Total Duration: {plan.get('total_duration', 'N/A')}")
    output.append("=" * 50)

    for phase in plan.get("phases", []):
        output.append(f"\nPHASE {phase['phase']}: {phase['title']}")
        output.append(f"Duration: {phase['duration']}")
        output.append(f"Goal: {phase['goal']}")
        output.append(f"Skills: {', '.join(phase['skills'])}")
        output.append("\nResources:")
        for r in phase.get("resources", []):
            output.append(f"  - [{r['type']}] {r['title']}")
            output.append(f"    URL: {r['url']}")
            output.append(f"    Time: {r['duration']} | Priority: {r['priority']}")

    if plan.get("adjacent_skills"):
        output.append(f"\nADJACENT SKILLS TO EXPLORE:")
        for skill in plan["adjacent_skills"]:
            output.append(f"  - {skill}")

    if plan.get("tips"):
        output.append(f"\nLEARNING TIPS:")
        for tip in plan["tips"]:
            output.append(f"  - {tip}")

    return "\n".join(output)


if __name__ == "__main__":
    from resume_parser import parse_job_description, parse_resume, identify_skill_gaps

    sample_jd = """
    We are looking for a Senior Python Developer with 3+ years of experience.
    Must have: Python, FastAPI, PostgreSQL, Docker
    Nice to have: Kubernetes, Redis, AWS
    Soft skills: Strong communication, team player
    """

    sample_resume = """
    John Doe - Software Developer (2 years experience)
    Skills: Python, Flask, MySQL, Git
    Projects: Built a REST API using Flask and MySQL
    """

    print("Generating learning plan...")
    jd = parse_job_description(sample_jd)
    resume = parse_resume(sample_resume)
    gaps = identify_skill_gaps(jd, resume)

    assessment_data = {
        "jd_data": jd,
        "resume_data": resume,
        "gaps_data": gaps,
        "assessed_skills": {
            "Python": {"proficiency": "Intermediate", "notes": "2 years Flask experience"}
        }
    }

    plan = generate_learning_plan(assessment_data)
    print(format_learning_plan(plan))