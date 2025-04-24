import json
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb+srv://VishalVarwani:Vishal123@vishalvarwanicluster0.jh3ewwl.mongodb.net/")
db = client["career_copilot"]
plan_collection = db["bootcamp_days"]

# Clear existing (optional)
plan_collection.delete_many({})  # Use with caution

# Load the JSON file
with open(r"C:\Users\Vishal\Desktop\hackathonqsummit\lewagon_bootcamp_topics_day_plan.json", "r") as f:
    bootcamp_data = json.load(f)

# Insert the 'days' list into the collection
plan_collection.insert_many(bootcamp_data["days"])
print("✅ Bootcamp day plan imported into MongoDB.")
