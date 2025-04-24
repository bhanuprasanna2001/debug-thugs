from pymongo import MongoClient
from datetime import datetime
import uuid

# Setup MongoDB
client = MongoClient("mongodb+srv://VishalVarwani:Vishal123@vishalvarwanicluster0.jh3ewwl.mongodb.net/")
db = client["career_copilot"]
plan_collection = db["bootcamp_days"]
reflection_collection = db["user_course_reflections"]

# User metadata
user_id = str(uuid.uuid4())
print(f"🆔 Generated User ID: {user_id}")
course_id = "lewagon_bootcamp"

# Ask for multiple days
day_input = input("📅 Enter the day numbers you want to reflect on (comma-separated): ")
days_to_reflect = [int(x.strip()) for x in day_input.split(',')]

# Predefined day-specific questions
day_questions = {
    1: [
        {
            "question": "How confident are you with the basic Git commands (clone, commit, push)?",
            "options": ["Very confident", "Somewhat confident", "A little unsure", "Not confident at all"]
        },
        {
            "question": "Which tool felt easiest to use?",
            "options": ["Terminal", "VSCode", "GitHub Desktop", "None of them"]
        },
        {
            "question": "Which tool felt most confusing?",
            "options": ["Terminal", "VSCode", "GitHub Desktop", "None of them"]
        }
    ],
    2: [
        {
            "question": "How comfortable do you feel with navigating folders using the terminal?",
            "options": ["Very comfortable", "Somewhat", "Still learning", "Not comfortable at all"]
        },
        {
            "question": "Which command felt most useful today?",
            "options": ["cd", "ls", "mkdir", "touch", "rm"]
        },
        {
            "question": "Did you enjoy using the terminal today?",
            "options": ["Yes", "It was okay", "Not really"]
        }
    ]
}

# Loop over each selected day
for day_number in days_to_reflect:
    today_plan = plan_collection.find_one({"day": day_number})

    if not today_plan:
        print(f"❌ No bootcamp plan found for Day {day_number}. Skipping...")
        continue

    module = today_plan.get("module")
    topic = today_plan.get("topic")
    skills = today_plan.get("skills", [])

    print(f"\n📚 Day {day_number}: {topic} ({module})")
    print("Skills covered today:")
    for idx, skill in enumerate(skills, 1):
        print(f"  {idx}. {skill}")

    # Select liked and disliked skills
    def select_skills(prompt):
        print(f"\n{prompt}")
        print("Enter comma-separated numbers (e.g. 1,3,5):")
        selected = input().split(',')
        selected_skills = []
        for num in selected:
            try:
                idx = int(num.strip()) - 1
                if 0 <= idx < len(skills):
                    selected_skills.append(skills[idx])
            except ValueError:
                continue
        return selected_skills

    liked_skills = select_skills("👍 Which skills did you enjoy today?")
    disliked_skills = select_skills("👎 Which skills did you struggle with or didn't enjoy?")

    # Collect custom comments
    comments = {}
    for skill in liked_skills + disliked_skills:
        reason = input(f"💬 Why did you feel this way about '{skill}'? ")
        comments[skill] = reason

    # Ask topic-specific multiple-choice questions
    extra_answers = {}
    if day_number in day_questions:
        print(f"\n📋 Topic-specific multiple-choice questions for Day {day_number}:")
        for item in day_questions[day_number]:
            question = item["question"]
            options = item["options"]

            print(f"\n{question}")
            for idx, opt in enumerate(options, 1):
                print(f"  {idx}. {opt}")

            while True:
                try:
                    choice = int(input("Select option number: "))
                    if 1 <= choice <= len(options):
                        extra_answers[question] = options[choice - 1]
                        break
                    else:
                        print("❌ Please enter a valid option number.")
                except ValueError:
                    print("❌ Please enter a number.")

    # Build reflection entry
    day_reflection = {
        "day": day_number,
        "topic": topic,
        "module": module,
        "skills": skills,
        "liked_skills": liked_skills,
        "disliked_skills": disliked_skills,
        "comments": comments,
        "extra_answers": extra_answers,
        "timestamp": datetime.utcnow()
    }

    # Insert or update user record
    reflection_collection.update_one(
        {"user_id": user_id, "course_id": course_id},
        {
            "$setOnInsert": {"user_id": user_id, "course_id": course_id},
            "$push": {"reflections": day_reflection}
        },
        upsert=True
    )

    print(f"✅ Reflection for Day {day_number} saved.\n")

print("🎉 All selected reflections complete and stored in MongoDB!")
