# 📋 Sample Inputs & Outputs

## Sample Input 1 — Job Description

We are looking for a Senior Python Developer with 3+ years of experience.
Must have:

Python
FastAPI
PostgreSQL
Docker

Nice to have:

Kubernetes
Redis
AWS

Soft skills: Strong communication, team player

## Sample Input 2 — Resume
John Doe - Software Developer (2 years experience)
Skills: Python, Flask, MySQL, Git
Projects:

Built a REST API using Flask and MySQL for an e-commerce platform
Developed data processing scripts using Python and Pandas

---

## Sample Output 1 — Skill Gap Analysis

```json
{
  "matched_skills": [
    {"skill": "Python", "importance": "must-have"}
  ],
  "skill_gaps": [
    {"skill": "FastAPI", "importance": "must-have"},
    {"skill": "PostgreSQL", "importance": "must-have"},
    {"skill": "Docker", "importance": "must-have"},
    {"skill": "Kubernetes", "importance": "nice-to-have"},
    {"skill": "Redis", "importance": "nice-to-have"},
    {"skill": "AWS", "importance": "nice-to-have"}
  ],
  "gap_count": 6,
  "match_count": 1,
  "total_required": 7
}
```

---

## Sample Output 2 — Conversational Assessment

🤖 Agent: Welcome! I'm Alex, your technical interviewer for the
Senior Python Developer role. Could you tell me your name?
👤 User:  Hi, I'm John.
🤖 Agent: Great to meet you John! Let's assess your Python skills.
Can you tell me about a project where you optimised Python
code performance for handling large datasets?
👤 User:  I used Python with Flask to build a REST API and handled
large CSV files using Pandas with chunking.
🤖 Agent: Great answer! Using chunking with Pandas is a solid
approach for memory efficiency.
Proficiency assessed: Intermediate

Overall: You have a solid Python foundation with 2 years
      of Flask experience. Key gaps are FastAPI, PostgreSQL,
      and Docker which are must-have for this role.

---

## Sample Output 3 — Personalised Learning Plan

PERSONALISED LEARNING PLAN
Total Duration: 16 weeks
PHASE 1: Foundation (2 weeks)
Goal: Learn FastAPI — adjacent to your Flask experience
Skills: FastAPI
Resources:

[Course] FastAPI Official Tutorial
URL: https://fastapi.tiangolo.com/tutorial/
Time: 10 hours | Priority: High
[Video] FastAPI Full Course - freeCodeCamp
URL: https://www.youtube.com/watch?v=0sOvCWFmrtA
Time: 4 hours | Priority: High

PHASE 2: Database (4 weeks)
Goal: Migrate from MySQL knowledge to PostgreSQL
Skills: PostgreSQL
Resources:

[Course] PostgreSQL Tutorial for Beginners
URL: https://www.postgresqltutorial.com/
Time: 15 hours | Priority: High

PHASE 3: Containerization (4 weeks)
Goal: Learn Docker for deployment
Skills: Docker
Resources:

[Course] Docker 101 Tutorial
URL: https://www.docker.com/101-tutorial
Time: 20 hours | Priority: High

PHASE 4: Nice-to-Have (6 weeks)
Goal: Kubernetes, Redis, AWS basics
Skills: Kubernetes, Redis, AWS
ADJACENT SKILLS TO EXPLORE:

SQLAlchemy (ORM for PostgreSQL)
Pydantic (used heavily in FastAPI)
GitHub Actions (CI/CD)

LEARNING TIPS:

Build a FastAPI + PostgreSQL + Docker project to combine all skills
Your Flask experience makes FastAPI learning 50% faster
Focus on must-have skills before nice-to-have


