![Header](./assets/pathly-header.jpg)
# Pathly – Your AI-Powered Reflection Copilot for Learning & Growth


> Pathly transforms daily skill reflections into personalized growth maps, course suggestions, and career paths using LLMs and RAG.


---

## 📚 Table of Contents

- [What It Does](#what-it-does)
- [Problem Statement](#problem-statement)
- [Our Solution](#our-solution)
- [Key Features](#key-features)
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [How to Run Locally](#how-to-run-locally)
- [Screenshots / Demo](#screenshots--demo)
- [Acknowledgements](#acknowledgements)


---

## What It Does
Pathly is a smart, LLM-powered learning assistant built for students enrolled in intensive bootcamps. It collects daily feedback on what skills learners enjoyed or struggled with, then processes this data using AI to:

- Summarize learning journeys
- Identify personal strengths and challenges
- Suggest growth areas and tech stacks
- Recommend courses
- Match potential career paths and jobs


---

## Problem Statement
- Bootcamp students are overloaded with daily content and tasks.
- They struggle to understand what they’re mastering versus what they’re missing.
- There’s no structured way to reflect, track skills, or connect daily progress to career readiness.
- Most learners finish with unclear strengths and no guided path forward.

---

## Our Solution
Pathly collects daily reflections from learners over a 50-day course. Each entry includes:
- Liked & disliked skills selected by the user
- Reasons for their preferences (entered as comments)
- Confidence levels and tool ratings via extra feedback questions

Daily entries are stored in MongoDB, and each day’s submission also updates the learner’s progress.

On Day 50:
- GPT-4 reads the entire reflection history and produces a personalized summary
- The summary includes: key strengths, areas of struggle, and learning style patterns
- This summary is passed to a RAG-powered recommender that uses FAISS to search a curated corpus of technical courses
- Based on retrieved content, the system suggests ideal next courses and growth paths

The platform also includes:
- A Resume Uploader that will extract core skills and maps the learner’s skills suggest the role one must be applying to.

Together, Pathly not only summarizes learning but actively suggests what to learn next and where to grow.

---

## Key Features
- Daily Skill Reflections with context
- Progress Tracking across 50 days
- LLM Summary Generator on Day 50 (GPT-4)
- Course Recommendations via RAG
- Job Suggestions using resume skills 

---

## Tech Stack
- **Frontend:** React
- **Backend:** Flask (Python)
- **Database:** MongoDB 
- **LLM Engine:** OpenAI GPT-4
- **RAG Pipeline:** FAISS + Embedded Course Corpus
- **Deployment:** (Local + GitHub Release)

---

## Architecture
![Architecture Diagram](./assets/architecture-pathly.png)

```mermaid
flowchart LR
  User[User] -->|Daily Review| MongoDB
  MongoDB --> LLM[LLM]
  LLM --> Summary[Summary]
  Summary --> Strengths
  Summary --> Weaknesses
  Summary --> Recommender
  Recommender --> FAISS[FAISS]
  FAISS --> CourseCorpus[Course Corpus]
  Recommender --> Courses
  Strengths --> Response
  Weaknesses --> Response
  Courses --> Response
  Response --> User
```

---

## How to Run Locally
```bash
# Frontend
cd frontend
npm install
npm start

# Backend
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
python app.py
```
Ensure you have a `.env` file with your MongoDB URI and OpenAI key.

---

## Screenshots / Demo
- ![Reflection Form](./assets/screenshot-form.png)
- ![Progress Tracker](./assets/screenshot-progress.png)
- ![Final Summary Dashboard](./assets/screenshot-summary.png)



---

## Acknowledgements
Acknowledgements

We’d like to extend our heartfelt thanks to *QHack Summit* and *Le Wagon* for providing the challenge and opportunity to build something impactful during this hackathon.

