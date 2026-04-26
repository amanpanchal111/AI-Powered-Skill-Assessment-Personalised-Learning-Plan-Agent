# 🤖 AI Skill Assessment & Personalised Learning Plan Agent

Project Overview

This platform automates the candidate screening process by matching uploaded resumes against Job Descriptions (JDs). It uses AI to extract skills, conduct automated conversational assessments to score proficiency, and generates a personalized learning roadmap for any identified skill gaps..

---

## 📸 Demo

### Step 1 — Upload JD & Resume
[Upload Screen](https://i.imgur.com/placeholder1.png)

### Step 2 — Skill Gap Analysis
[Analysis Screen](https://i.imgur.com/placeholder2.png)

### Step 3 — Conversational Assessment
[Chat Screen](https://i.imgur.com/placeholder3.png)

### Step 4 — Personalised Learning Plan
[Learning Plan](https://i.imgur.com/placeholder4.png)

---

## ✨ Key Features

| Feature | Description |
|---|---|
| 📄 **Resume Parsing** | Supports PDF, DOCX, and TXT formats |
| 📋 **JD Analysis** | Extracts must-have and nice-to-have skills |
| 🔍 **Skill Gap Detection** | Compares resume skills vs JD requirements |
| 💬 **Conversational Assessment** | AI interviews candidate per skill in real-time |
| 📊 **Proficiency Scoring** | Rates each skill as Beginner / Intermediate / Advanced |
| 📚 **Learning Plan** | Phased plan with real resources, URLs and time estimates |
| ⚡ **Fast & Free** | Powered by Groq's LLaMA 3.3 70B — no billing required |

---

## 🛠️ Tech Stack

Backend        →  Python 3.10+, Flask
AI Model       →  LLaMA 3.3 70B via Groq API
Resume Parser  →  PyPDF2, python-docx
Frontend       →  HTML5, CSS3, Vanilla JavaScript
Environment    →  python-dotenv

---

## 📁 Project Structure

skill-assessment-agent/
│
├── app.py                  # Flask web server & API routes
├── agent.py                # Core conversational AI assessment agent
├── resume_parser.py        # Resume & JD parsing + skill gap detection
├── learning_plan.py        # Personalised learning plan generator
│
├── templates/
│   └── index.html          # Full frontend UI
│
├── uploads/                # Temporary resume file storage
├── requirements.txt        # Python dependencies
├── .env                    # API keys (not committed)
├── .gitignore
└── README.md

---

## ⚙️ Local Setup Instructions

### Prerequisites
- Python 3.10 or higher
- Git
- A free Groq API key → [console.groq.com/keys](https://console.groq.com/keys)

---

### Step 1 — Clone the repository

```bash
git clone https://github.com/yourusername/skill-assessment-agent.git
cd skill-assessment-agent
```

---

### Step 2 — Create and activate virtual environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

---

### Step 3 — Install dependencies

```bash
pip install -r requirements.txt
```

---

### Step 4 — Configure environment variables

Create a `.env` file in the root directory:

```env
GROQ_API_KEY=gsk_*************************```

> 🔑 Get your **free** Groq API key at [console.groq.com/keys](https://console.groq.com/keys)
> No credit card required.

---

### Step 5 — Run the application

```bash
python app.py
```

---

### Step 6 — Open in browser

http://localhost:5000

---

## 🎯 How It Works

┌─────────────────────────────────────────────────────────┐
│                                                         │
│   1. UPLOAD      →   Paste JD + Resume or upload file  │
│                                                         │
│   2. ANALYSIS    →   AI extracts & compares skills      │
│                      Identifies must-have gaps          │
│                                                         │
│   3. ASSESSMENT  →   Conversational interview per skill │
│                      Scores: Beginner/Intermediate/     │
│                      Advanced                           │
│                                                         │
│   4. LEARNING    →   Phased learning plan               │
│      PLAN            Real URLs, time estimates,         │
│                      adjacent skills                    │
│                                                         │
└─────────────────────────────────────────────────────────┘

---

## 🤖 AI Agent Architecture

resume_parser.py
├── extract_text_from_file()     # PDF / DOCX / TXT
├── parse_job_description()      # Extract JD skills via LLM
├── parse_resume()               # Extract resume skills via LLM
└── identify_skill_gaps()        # Gap analysis
agent.py (SkillAssessmentAgent)
├── start_assessment()           # Greeting + intro
├── assess_next_skill()          # Per-skill question
├── process_answer()             # Evaluate + score answer
└── generate_summary()           # Overall assessment summary
learning_plan.py
├── generate_learning_plan()     # Phased plan via LLM
└── format_learning_plan()       # Text formatter
app.py (Flask)
├── POST /upload                 # Parse JD + Resume
├── POST /start_assessment       # Begin chat session
├── POST /chat                   # Handle conversation
└── GET  /learning_plan          # Generate plan

---

## 📦 Requirements

```txt
flask
groq
PyPDF2
python-docx
python-dotenv
```

Install all with:
```bash
pip install -r requirements.txt
```

---

## 🔐 Environment Variables

| Variable | Description | Required |
|---|---|---|
| `GROQ_API_KEY` | Groq API key for LLaMA model | ✅ Yes |

---

## 🚀 Deployment

To deploy on a server:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

For platforms like **Render** or **Railway**:
- Set `GROQ_API_KEY` as an environment variable
- Set start command to `gunicorn app:app`

---

## 👨‍💻 Author

**Your Name**
- GitHub: [amanpanchal111](https://github.com/yourusername)
- LinkedIn: [https://www.linkedin.com/in/aman-panchal-b31829231](https://linkedin.com/in/https://www.linkedin.com/in/aman-panchal-b31829231)

---

## 🌐 Live Demo
👉 **[Click here to use the app](https://resume-skillcheck-ai.streamlit.app/)**
> No installation required — just open and use!
> Built with using Python, Flask, and Groq LLaMA 3.3 70B