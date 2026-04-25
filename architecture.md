# 🏗️ Architecture & Scoring Logic

## System Architecture

┌─────────────────────────────────────────────────────────────────┐
│                        USER BROWSER                             │
│                     (index.html - UI)                           │
└────────────────────────┬────────────────────────────────────────┘
│ HTTP Requests
▼
┌─────────────────────────────────────────────────────────────────┐
│                     FLASK WEB SERVER                            │
│                        (app.py)                                 │
│                                                                 │
│   POST /upload          →  Parse JD + Resume                   │
│   POST /start_assessment →  Begin AI Interview                  │
│   POST /chat            →  Handle Conversation                  │
│   GET  /learning_plan   →  Generate Learning Plan               │
└────┬──────────────┬──────────────┬──────────────────────────────┘
│              │              │
▼              ▼              ▼
┌─────────┐  ┌──────────┐  ┌─────────────────┐
│ resume_ │  │ agent.py │  │ learning_plan.py│
│parser.py│  │          │  │                 │
│         │  │ Conversa-│  │ Generates       │
│ Extracts│  │ tional   │  │ phased learning │
│ skills  │  │ AI inter-│  │ plan with       │
│ from JD │  │ viewer   │  │ resources       │
│ & Resume│  │          │  │                 │
└────┬────┘  └────┬─────┘  └────────┬────────┘
│             │                 │
└─────────────┴─────────────────┘
│
▼
┌─────────────────────────────┐
│        GROQ API             │
│   LLaMA 3.3 70B Model       │
│                             │
│  - Skill extraction         │
│  - Question generation      │
│  - Answer evaluation        │
│  - Plan generation          │
└─────────────────────────────┘

## 🧠 Scoring & Assessment Logic

### Step 1 — Skill Extraction
- JD text is sent to LLaMA 3.3 70B
- Model returns structured JSON with skills tagged as `must-have` or `nice-to-have`
- Resume text is parsed similarly to extract candidate's current skills

### Step 2 — Gap Analysis
For each skill in JD:
if skill exists in resume → MATCHED
else → GAP (tagged as must-have or nice-to-have)
Score = matched_skills / total_required_skills × 100

### Step 3 — Conversational Assessment
- Only matched skills are assessed (candidate claims to know them)
- Agent asks ONE practical question per skill
- Candidate's answer is evaluated by LLaMA with this rubric:

Beginner     → Knows concepts but limited practical experience
Intermediate → Has applied the skill in real projects
Advanced     → Deep expertise, can handle complex scenarios

### Step 4 — Learning Plan Generation
- Gaps are prioritised: must-have first, nice-to-have second
- Adjacent skills are identified based on candidate's existing stack
- Resources are curated from: official docs, freeCodeCamp, Udemy, YouTube
- Time estimates are realistic based on skill complexity

## 📊 Proficiency Scoring Rubric

| Score | Level | Criteria |
|---|---|---|
| 1 | Beginner | Theoretical knowledge only |
| 2 | Intermediate | Applied in projects, some experience |
| 3 | Advanced | Deep expertise, production experience |

## 🔄 Data Flow

Input: JD Text + Resume Text/File
│
▼
LLM Parsing → Structured JSON (skills, gaps)
│
▼
Gap Analysis → Matched vs Missing skills
│
▼
Conversational Assessment → Proficiency scores
│
▼
Learning Plan → Phased roadmap with resources
│
▼
Output: Personalised Learning Plan (phases, URLs, time)

