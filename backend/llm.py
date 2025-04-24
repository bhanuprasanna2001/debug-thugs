import json
import openai
from pymongo import MongoClient
from openai import OpenAI

# Set your API key (best via environment variable in production)
client = OpenAI(api_key="")



# 1 — Load the daily feedback that was saved as feedback.json
with open(r"C:\Users\Vishal\Desktop\hackathonqsummit\backend\feedback_50_days.json", "r", encoding="utf-8") as f:
    user_doc = json.load(f)

# 2 — Re-create your formatted_reflections block
formatted_reflections = ""
for r in user_doc:                                      # top level is already a list
    formatted_reflections += f"Day {r['day']}\n"
    formatted_reflections += f"  Liked: {', '.join(r.get('likes', []) or ['None'])}\n"
    formatted_reflections += f"  Disliked: {', '.join(r.get('dislikes', []) or ['None'])}\n"
    # like_reasons + dislike_reasons to replicate “comments”
    comments = {**r.get("like_reasons", {}), **r.get("dislike_reasons", {})}
    for skill, comment in comments.items():
        formatted_reflections += f"    • {skill}: {comment}\n"
    formatted_reflections += "\n"

# 3 — Prompt that forces JSON output
prompt = f"""
You are a career-guidance assistant.

Analyse the student's daily reflections and reply **ONLY** with valid JSON
containing these keys (and no additional text):

{{
  "user_id": "{user_doc[0]['user_id']}",   // unique identifier for the student
  "strengths":            [string, …],   // skills or behaviors going well
  "challenges":           [string, …],   // skills or behaviors the student struggles with
  "weekly_recommendations":[string, …],   // concise, actionable suggestions for the next 5-7 days
  "potential_career_paths":[             // 2-4 career ideas that fit the strengths
    {{
      "title":  string,                  // e.g. "Front-End Developer"
      "reason": string                   // one-sentence rationale tied to reflections
    }},
    …
  ]
}}

Reflections:
{formatted_reflections}
"""

import tiktoken

def num_tokens_gpt(text: str, model: str = "gpt-4o-mini") -> int:
    """
    Return the number of tokens an OpenAI model will use for `text`.
    """
    enc = tiktoken.encoding_for_model(model)   # falls back to cl100k_base if unknown
    return len(enc.encode(text))

print("Token count:", num_tokens_gpt(prompt))

# Count tokens


# Send to OpenAI GPT-4

response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a helpful, thoughtful career-guidance assitant."},
        {"role": "user", "content": prompt}
    ]
)

summary = response.choices[0].message.content
print("\n🧠 Weekly Learning Summary:\n")
print(summary)