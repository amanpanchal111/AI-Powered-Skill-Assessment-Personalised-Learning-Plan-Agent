import os
import json
from flask import Flask, render_template, request, jsonify, session
from dotenv import load_dotenv
from resume_parser import parse_job_description, parse_resume, identify_skill_gaps, extract_text_from_file
from agent import SkillAssessmentAgent
from learning_plan import generate_learning_plan, format_learning_plan

load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/")
def index():
    session.clear()
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    try:
        jd_text = request.form.get("jd_text", "").strip()
        resume_file = request.files.get("resume_file")
        resume_text = request.form.get("resume_text", "").strip()

        if not jd_text:
            return jsonify({"error": "Please provide a job description"}), 400

        if resume_file and resume_file.filename:
            filename = resume_file.filename
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            resume_file.save(filepath)
            resume_text = extract_text_from_file(filepath)

        if not resume_text:
            return jsonify({"error": "Please provide a resume"}), 400

        jd_data = parse_job_description(jd_text)
        resume_data = parse_resume(resume_text)
        gaps_data = identify_skill_gaps(jd_data, resume_data)

        session["jd_data"] = jd_data
        session["resume_data"] = resume_data
        session["gaps_data"] = gaps_data
        session["conversation_history"] = []
        session["assessed_skills"] = {}
        session["current_skill_index"] = 0
        session["assessment_complete"] = False

        return jsonify({
            "success": True,
            "jd_data": jd_data,
            "resume_data": resume_data,
            "gaps_data": gaps_data
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/start_assessment", methods=["POST"])
def start_assessment():
    try:
        jd_data = session.get("jd_data")
        resume_data = session.get("resume_data")
        gaps_data = session.get("gaps_data")

        if not jd_data:
            return jsonify({"error": "Please upload JD and resume first"}), 400

        agent = SkillAssessmentAgent(jd_data, resume_data, gaps_data)
        greeting = agent.start_assessment()
        first_question = agent.assess_next_skill()

        session["conversation_history"] = agent.conversation_history
        session["assessed_skills"] = agent.assessed_skills
        session["current_skill_index"] = agent.current_skill_index
        session["assessment_complete"] = agent.assessment_complete

        return jsonify({
            "success": True,
            "message": greeting + "\n\n" + first_question
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_message = request.json.get("message", "").strip()
        if not user_message:
            return jsonify({"error": "Empty message"}), 400

        jd_data = session.get("jd_data")
        resume_data = session.get("resume_data")
        gaps_data = session.get("gaps_data")
        conversation_history = session.get("conversation_history", [])
        assessed_skills = session.get("assessed_skills", {})
        current_skill_index = session.get("current_skill_index", 0)
        assessment_complete = session.get("assessment_complete", False)

        if assessment_complete:
            return jsonify({
                "message": "Assessment is complete! Please view your learning plan below.",
                "assessment_complete": True
            })

        agent = SkillAssessmentAgent(jd_data, resume_data, gaps_data)
        agent.conversation_history = conversation_history
        agent.assessed_skills = assessed_skills
        agent.current_skill_index = current_skill_index
        agent.assessment_complete = assessment_complete

        response = agent.process_answer(user_message)

        session["conversation_history"] = agent.conversation_history
        session["assessed_skills"] = agent.assessed_skills
        session["current_skill_index"] = agent.current_skill_index
        session["assessment_complete"] = agent.assessment_complete

        return jsonify({
            "message": response,
            "assessment_complete": agent.assessment_complete,
            "assessed_skills": agent.assessed_skills
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/learning_plan", methods=["GET"])
def learning_plan():
    try:
        jd_data = session.get("jd_data")
        resume_data = session.get("resume_data")
        gaps_data = session.get("gaps_data")
        assessed_skills = session.get("assessed_skills", {})

        if not jd_data:
            return jsonify({"error": "No assessment data found"}), 400

        assessment_data = {
            "jd_data": jd_data,
            "resume_data": resume_data,
            "gaps_data": gaps_data,
            "assessed_skills": assessed_skills
        }

        plan = generate_learning_plan(assessment_data)

        return jsonify({
            "success": True,
            "plan": plan,
            "formatted": format_learning_plan(plan)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)