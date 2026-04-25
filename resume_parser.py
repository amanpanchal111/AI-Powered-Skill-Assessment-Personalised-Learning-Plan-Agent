import os
import json
import PyPDF2
import docx
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY").strip())

def call_groq(prompt):
    """Call Groq API and return parsed JSON response."""
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )
    raw = response.choices[0].message.content.strip()
    raw = raw.replace("```json", "").replace("```", "").strip()
    return json.loads(raw)


def extract_text_from_pdf(file_path):
    """Extract text from a PDF file."""
    text = ""
    try:
        with open(file_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text() + "\n"
    except Exception as e:
        print(f"PDF extraction error: {e}")
    return text.strip()


def extract_text_from_docx(file_path):
    """Extract text from a DOCX file."""
    text = ""
    try:
        doc = docx.Document(file_path)
        for para in doc.paragraphs:
            text += para.text + "\n"
    except Exception as e:
        print(f"DOCX extraction error: {e}")
    return text.strip()


def extract_text_from_file(file_path):
    """Auto-detect file type and extract text."""
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
        return extract_text_from_pdf(file_path)
    elif ext == ".docx":
        return extract_text_from_docx(file_path)
    elif ext == ".txt":
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read().strip()
    else:
        return ""


def parse_job_description(jd_text):
    """Use Groq to extract required skills from a Job Description."""
    prompt = f"""
You are an expert HR analyst. Analyze the following Job Description and extract:
1. Required technical skills (with importance: must-have / nice-to-have)
2. Required soft skills
3. Years of experience needed
4. Role title and seniority level

Return ONLY a valid JSON object in this exact format with no extra text:
{{
  "role_title": "...",
  "seniority": "...",
  "experience_years": "...",
  "technical_skills": [
    {{"skill": "Python", "importance": "must-have"}},
    {{"skill": "Docker", "importance": "nice-to-have"}}
  ],
  "soft_skills": ["Communication", "Teamwork"]
}}

Job Description:
{jd_text}
"""
    return call_groq(prompt)


def parse_resume(resume_text):
    """Use Groq to extract skills and experience from a Resume."""
    prompt = f"""
You are an expert HR analyst. Analyze the following Resume and extract:
1. All technical skills mentioned
2. Soft skills demonstrated
3. Total years of experience
4. Most recent job title
5. Key projects or achievements

Return ONLY a valid JSON object in this exact format with no extra text:
{{
  "current_title": "...",
  "total_experience_years": "...",
  "technical_skills": ["Python", "SQL", "React"],
  "soft_skills": ["Leadership", "Problem Solving"],
  "projects": ["Built a REST API for...", "Led a team of 5..."]
}}

Resume:
{resume_text}
"""
    return call_groq(prompt)


def identify_skill_gaps(jd_data, resume_data):
    """Compare JD requirements vs Resume skills to find gaps."""
    resume_skills = [s.lower() for s in resume_data.get("technical_skills", [])]

    gaps = []
    matched = []

    for skill_obj in jd_data.get("technical_skills", []):
        skill = skill_obj["skill"]
        importance = skill_obj["importance"]
        if skill.lower() in resume_skills:
            matched.append({"skill": skill, "importance": importance})
        else:
            gaps.append({"skill": skill, "importance": importance})

    return {
        "matched_skills": matched,
        "skill_gaps": gaps,
        "gap_count": len(gaps),
        "match_count": len(matched),
        "total_required": len(jd_data.get("technical_skills", []))
    }


if __name__ == "__main__":
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

    print("Parsing JD...")
    jd = parse_job_description(sample_jd)
    print("JD:", json.dumps(jd, indent=2))

    print("\nParsing Resume...")
    resume = parse_resume(sample_resume)
    print("Resume:", json.dumps(resume, indent=2))

    print("\nIdentifying Gaps...")
    gaps = identify_skill_gaps(jd, resume)
    print("Gaps:", json.dumps(gaps, indent=2))