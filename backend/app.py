from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime
from openai import OpenAI
import json
import re
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier

app = Flask(__name__)
CORS(app)

# OpenAI setup
client = OpenAI(api_key="")

# Mongo setup
mongo = MongoClient("mongodb+srv://jadhavgourav98:Vishal123@vishalvarwanicluster0.jh3ewwl.mongodb.net/")
db = mongo["career_copilot"]
plan_collection = db["bootcamp_days"]
reflection_collection = db["user_course_reflections"]

# Resume recommendation model
df = pd.read_csv(r"C:\Users\Vishal\Desktop\resume\jobs_dataset_with_features.csv")
min_count = 6500
df = df[df['Role'].isin(df['Role'].value_counts()[lambda x: x >= min_count].index)].reset_index(drop=True)
df = df.sample(n=30000, random_state=42)

tfidf_vectorizer = TfidfVectorizer()
X = tfidf_vectorizer.fit_transform(df['Features'])
y = df['Role']
rf_classifier = RandomForestClassifier()
rf_classifier.fit(X, y)

def clean_resume(txt):
    txt = re.sub(r'http\S+', ' ', txt)
    txt = re.sub(r'RT|cc', ' ', txt)
    txt = re.sub(r'#\S+', ' ', txt)
    txt = re.sub(r'@\S+', ' ', txt)
    txt = re.sub(r'[^\w\s]', ' ', txt)
    txt = re.sub(r'[^\x00-\x7f]', ' ', txt)
    txt = re.sub(r'\s+', ' ', txt)
    return txt.strip()

@app.route("/api/bootcamp-day/<int:day>", methods=["GET"])
def get_bootcamp_day(day):
    plan = plan_collection.find_one({"day": day})
    if not plan:
        return jsonify({"error": "Day not found"}), 404

    questions = {
        1: [{"question": "How confident are you with Git?", "options": ["Very", "Somewhat", "Not"]}],
        2: [{"question": "Did you enjoy the terminal?", "options": ["Yes", "No"]}]
    }

    return jsonify({
        "day": day,
        "module": plan.get("module"),
        "topic": plan.get("topic"),
        "skills": plan.get("skills", []),
        "questions": questions.get(day, [])
    })

@app.route("/api/save-reflection", methods=["POST"])
def save_reflection():
    data = request.get_json()
    reflection = {
        "day": data["day"],
        "topic": data["topic"],
        "module": data["module"],
        "skills": data["skills"],
        "liked_skills": data["liked_skills"],
        "disliked_skills": data["disliked_skills"],
        "comments": data["comments"],
        "extra_answers": data["extra_answers"],
        "timestamp": datetime.utcnow()
    }

    reflection_collection.update_one(
        {"user_id": data["user_id"], "course_id": data["course_id"]},
        {
            "$setOnInsert": {"user_id": data["user_id"], "course_id": data["course_id"]},
            "$push": {"reflections": reflection}
        },
        upsert=True
    )

    return jsonify({"message": "Reflection saved"}), 200

@app.route("/api/llm-summary", methods=["GET"])
def get_llm_summary():
    with open(r"C:\Users\Vishal\Desktop\hackathonqsummit\backend\feedback_50_days.json", "r", encoding="utf-8") as f:
        user_doc = json.load(f)

    user_id = user_doc.get("user_id")
    reflections = user_doc.get("reflections", [])

    formatted_reflections = ""
    for r in reflections:
        formatted_reflections += f"Day {r['day']}\n"
        formatted_reflections += f"  Liked: {', '.join(r.get('likes', []) or ['None'])}\n"
        formatted_reflections += f"  Disliked: {', '.join(r.get('dislikes', []) or ['None'])}\n"
        comments = {**r.get("like_reasons", {}), **r.get("dislike_reasons", {})}
        for skill, comment in comments.items():
            formatted_reflections += f"    • {skill}: {comment}\n"
        formatted_reflections += "\n"

    prompt = f"""
You are a career-guidance assistant.

Your task is to analyze the student's daily reflections and return a structured JSON object with key insights.

The student's unique identifier is: {user_id}

You must return **only** valid JSON in this exact format:

{{
  "user_id": "{user_id}",
  "strengths": [string, ...],
  "challenges": [string, ...],
  "weekly_recommendations": [string, ...],
  "potential_career_paths": [
    {{
      "title": string,
      "reason": string
    }},
    ...
  ]
}}

Reflections:
{formatted_reflections}
"""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful, thoughtful career-guidance assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    try:
        parsed_json = json.loads(response.choices[0].message.content)
        parsed_json["user_id"] = user_id
        return jsonify(parsed_json)
    except Exception as e:
        return jsonify({"error": "Failed to parse GPT response", "details": str(e)}), 500

@app.route("/api/user-progress/<user_id>", methods=["GET"])
def get_user_progress(user_id):
    user_doc = reflection_collection.find_one({"user_id": user_id})
    if not user_doc:
        return jsonify({"completed": 0, "total": 50, "percent": 0})

    completed = len(user_doc.get("reflections", []))
    total_days = 50
    percent = round((completed / total_days) * 100, 2)

    return jsonify({
        "completed": completed,
        "total": total_days,
        "percent": percent
    })

@app.route("/api/job-recommendation", methods=["POST"])
def recommend_job():
    data = request.get_json()
    resume_text = data.get("resume_text", "")

    if not resume_text.strip():
        return jsonify({"error": "No resume text provided."}), 400

    cleaned = clean_resume(resume_text)
    tfidf_input = tfidf_vectorizer.transform([cleaned])
    prediction = rf_classifier.predict(tfidf_input)[0]

    return jsonify({"predicted_category": prediction})

if __name__ == "__main__":
    app.run(debug=True)
