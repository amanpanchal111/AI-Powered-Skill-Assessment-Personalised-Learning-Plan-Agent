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

class SkillAssessmentAgent:
    def __init__(self, jd_data, resume_data, gaps_data):
        self.jd_data = jd_data
        self.resume_data = resume_data
        self.gaps_data = gaps_data
        self.conversation_history = []
        self.assessed_skills = {}
        self.current_skill_index = 0
        self.skills_to_assess = self._get_skills_to_assess()
        self.assessment_complete = False

    def _get_skills_to_assess(self):
        """Get list of skills to assess — matched skills only."""
        skills = []
        for skill in self.gaps_data.get("matched_skills", []):
            skills.append(skill["skill"])
        return skills

    def _call_groq(self, messages):
        """Call Groq API with conversation history."""
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            max_tokens=1000,
            messages=messages
        )
        return response.choices[0].message.content.strip()

    def start_assessment(self):
        """Start the conversational assessment."""
        role = self.jd_data.get("role_title", "the role")
        name_prompt = f"""You are a friendly but professional technical interviewer assessing a candidate for the role of {role}.

Start by warmly greeting the candidate, briefly explaining that you will assess their skills through conversation, and ask for their name."""

        self.conversation_history = [
            {"role": "system", "content": name_prompt}
        ]

        response = self._call_groq(self.conversation_history)
        self.conversation_history.append({"role": "assistant", "content": response})
        return response

    def assess_next_skill(self):
        """Move to assessing the next skill."""
        if self.current_skill_index >= len(self.skills_to_assess):
            self.assessment_complete = True
            return self.generate_summary()

        skill = self.skills_to_assess[self.current_skill_index]
        role = self.jd_data.get("role_title", "the role")

        question_prompt = f"""You are assessing the candidate's proficiency in '{skill}' for the role of {role}.

Ask ONE specific, practical technical question about '{skill}' that helps gauge their real experience level.
Keep the question conversational and clear. Do not ask multiple questions at once."""

        messages = self.conversation_history + [
            {"role": "user", "content": question_prompt}
        ]

        response = self._call_groq(messages)
        self.conversation_history.append({"role": "assistant", "content": response})
        return response

    def process_answer(self, user_answer):
        """Process candidate's answer and evaluate proficiency."""
        self.conversation_history.append({"role": "user", "content": user_answer})

        if self.current_skill_index >= len(self.skills_to_assess):
            self.assessment_complete = True
            return self.generate_summary()

        skill = self.skills_to_assess[self.current_skill_index]

        eval_prompt = f"""Based on the candidate's answer about '{skill}', do two things:

1. Evaluate their proficiency level as one of: Beginner / Intermediate / Advanced
2. Give a brief, encouraging follow-up response (1-2 sentences) acknowledging their answer

Then return a JSON object at the end in this exact format:
{{"skill": "{skill}", "proficiency": "Intermediate", "notes": "brief observation"}}"""

        messages = self.conversation_history + [
            {"role": "user", "content": eval_prompt}
        ]

        response = self._call_groq(messages)

        try:
            start = response.rfind("{")
            end = response.rfind("}") + 1
            if start != -1 and end != 0:
                json_str = response[start:end]
                skill_data = json.loads(json_str)
                self.assessed_skills[skill] = skill_data
                feedback = response[:start].strip()
            else:
                feedback = response
                self.assessed_skills[skill] = {
                    "skill": skill,
                    "proficiency": "Intermediate",
                    "notes": "Assessment recorded"
                }
        except Exception:
            feedback = response
            self.assessed_skills[skill] = {
                "skill": skill,
                "proficiency": "Intermediate",
                "notes": "Assessment recorded"
            }

        self.conversation_history.append({"role": "assistant", "content": feedback})
        self.current_skill_index += 1

        if self.current_skill_index < len(self.skills_to_assess):
            next_skill_response = self.assess_next_skill()
            return feedback + "\n\n" + next_skill_response
        else:
            self.assessment_complete = True
            summary = self.generate_summary()
            return feedback + "\n\n" + summary

    def generate_summary(self):
        """Generate assessment summary."""
        summary_data = {
            "assessed_skills": self.assessed_skills,
            "skill_gaps": self.gaps_data.get("skill_gaps", []),
            "total_skills_required": self.gaps_data.get("total_required", 0),
            "skills_matched": self.gaps_data.get("match_count", 0),
            "skills_missing": self.gaps_data.get("gap_count", 0)
        }

        prompt = f"""Based on this assessment data, write a brief professional summary (3-4 sentences) for the candidate:

Assessment Results: {json.dumps(summary_data, indent=2)}

Include:
- Overall impression
- Key strengths
- Main areas to improve
- Encouragement"""

        messages = [{"role": "user", "content": prompt}]
        summary = self._call_groq(messages)
        return summary

    def get_assessment_data(self):
        """Return all assessment data for learning plan generation."""
        return {
            "jd_data": self.jd_data,
            "resume_data": self.resume_data,
            "gaps_data": self.gaps_data,
            "assessed_skills": self.assessed_skills,
            "assessment_complete": self.assessment_complete
        }


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

    print("Setting up assessment...")
    jd = parse_job_description(sample_jd)
    resume = parse_resume(sample_resume)
    gaps = identify_skill_gaps(jd, resume)

    agent = SkillAssessmentAgent(jd, resume, gaps)

    print("\n--- ASSESSMENT START ---\n")
    print(agent.start_assessment())

    print("\n--- ASSESSING FIRST SKILL ---\n")
    print(agent.assess_next_skill())

    print("\n--- SIMULATING ANSWER ---\n")
    response = agent.process_answer("I have been using Python for 2 years, mainly for building REST APIs with Flask.")
    print(response)