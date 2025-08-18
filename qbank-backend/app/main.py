from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import random
import numpy as np

app = FastAPI(title="QBank API", version="1.0.0")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage (replace with database in production)
questions_db = []
sessions = {}

class Question(BaseModel):
    id: int
    text: str
    options: List[str]
    correct: int
    topic: str
    difficulty: float
    a: float = 1.0  # IRT discrimination
    b: float = 0.0  # IRT difficulty
    c: float = 0.2  # IRT guessing

class QuizConfig(BaseModel):
    num_questions: int = 20
    mode: str = "adaptive"
    topic: Optional[str] = None

class Answer(BaseModel):
    question_id: int
    selected: int

@app.on_event("startup")
async def startup():
    """Initialize question database"""
    global questions_db
    
    # Generate sample questions
    topics = ["math", "science", "english"]
    for i in range(5000):
        topic = topics[i % 3]
        questions_db.append({
            "id": i,
            "text": f"Question {i}: This is a {topic} question",
            "options": [f"Option A", f"Option B", f"Option C", f"Option D"],
            "correct": i % 4,
            "topic": topic,
            "difficulty": random.random(),
            "a": 0.5 + random.random() * 2,
            "b": -2 + random.random() * 4,
            "c": random.random() * 0.3
        })

@app.get("/")
async def root():
    return {"message": "QBank API is running", "total_questions": len(questions_db)}

@app.post("/api/quiz/start")
async def start_quiz(config: QuizConfig):
    """Start a new quiz session"""
    session_id = str(random.randint(10000, 99999))
    
    # Select questions
    filtered = questions_db
    if config.topic:
        filtered = [q for q in questions_db if q["topic"] == config.topic]
    
    selected = random.sample(filtered, min(config.num_questions, len(filtered)))
    
    sessions[session_id] = {
        "questions": selected,
        "current": 0,
        "responses": [],
        "theta": 0.0,
        "mode": config.mode
    }
    
    return {
        "session_id": session_id,
        "first_question": selected[0] if selected else None,
        "total_questions": len(selected)
    }

@app.get("/api/quiz/{session_id}/next")
async def get_next_question(session_id: str):
    """Get next question in quiz"""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session = sessions[session_id]
    if session["current"] >= len(session["questions"]):
        return {"completed": True, "score": calculate_score(session)}
    
    question = session["questions"][session["current"]]
    return {
        "question": question,
        "position": session["current"] + 1,
        "total": len(session["questions"])
    }

@app.post("/api/quiz/{session_id}/answer")
async def submit_answer(session_id: str, answer: Answer):
    """Submit answer and get next question"""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session = sessions[session_id]
    question = session["questions"][session["current"]]
    is_correct = answer.selected == question["correct"]
    
    # Store response
    session["responses"].append({
        "question_id": answer.question_id,
        "selected": answer.selected,
        "correct": question["correct"],
        "is_correct": is_correct
    })
    
    # Update theta for adaptive mode
    if session["mode"] == "adaptive":
        # Simple IRT update
        p = 1 / (1 + np.exp(-question["a"] * (session["theta"] - question["b"])))
        session["theta"] += (1 if is_correct else 0 - p) * 0.3
        session["theta"] = max(-3, min(3, session["theta"]))
    
    session["current"] += 1
    
    return {
        "correct": is_correct,
        "correct_answer": question["correct"],
        "theta": session["theta"],
        "next_question": session["questions"][session["current"]] if session["current"] < len(session["questions"]) else None
    }

@app.get("/api/quiz/{session_id}/results")
async def get_results(session_id: str):
    """Get quiz results"""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session = sessions[session_id]
    correct = sum(1 for r in session["responses"] if r["is_correct"])
    total = len(session["responses"])
    
    return {
        "score": (correct / total * 100) if total > 0 else 0,
        "correct": correct,
        "total": total,
        "theta": session["theta"],
        "responses": session["responses"]
    }

def calculate_score(session):
    correct = sum(1 for r in session["responses"] if r["is_correct"])
    total = len(session["responses"])
    return (correct / total * 100) if total > 0 else 0

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)