
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional, Set
import json
import os
import math
from datetime import datetime, timedelta

# Load data
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

def load_json(name: str):
    with open(os.path.join(DATA_DIR, name), "r") as f:
        return json.load(f)

# Load all data
SKILLS = {s["skill_id"]: s for s in load_json("skills.json")}
MODULES = load_json("modules.json")
RESOURCES = load_json("resources.json")

# Index resources by skill
RES_BY_SKILL: Dict[str, List[Dict[str, Any]]] = {}
for r in RESOURCES:
    for sid in r["skills"]:
        RES_BY_SKILL.setdefault(sid, []).append(r)

# Career path definitions
CAREER_PATHS = {
    "ml-engineer": {
        "name": "Machine Learning Engineer",
        "target_skills": [
            "math.linear_algebra", "math.statistics", "prog.python.advanced",
            "cs.ai.ml.basics", "cs.ai.deep_learning", "data.engineering",
            "cs.software.engineering", "cs.distributed"
        ],
        "description": "Build and deploy ML systems at scale"
    },
    "data-engineer": {
        "name": "Data Engineer",
        "target_skills": [
            "prog.python.advanced", "cs.databases", "data.engineering",
            "data.big_data", "data.streaming", "cs.distributed"
        ],
        "description": "Design and build data pipelines"
    },
    "embedded-engineer": {
        "name": "Embedded Systems Engineer",
        "target_skills": [
            "prog.c.basics", "ee.digital_logic", "ee.embedded",
            "cs.computer.arch", "cs.os"
        ],
        "description": "Develop firmware and embedded systems"
    },
    "full-stack": {
        "name": "Full Stack Developer",
        "target_skills": [
            "prog.javascript.basics", "cs.web.frontend", "cs.web.backend",
            "cs.databases", "cs.software.engineering"
        ],
        "description": "Build end-to-end web applications"
    },
    "security-engineer": {
        "name": "Security Engineer",
        "target_skills": [
            "cs.security.basics", "cs.security.crypto", "cs.security.web",
            "cs.networks", "cs.os"
        ],
        "description": "Secure systems and applications"
    }
}

# Major target skills
MAJOR_TARGETS = {
    "cs": [
        "prog.python.basics", "prog.c.basics", "math.discrete", "cs.ds.algorithms",
        "cs.computer.arch", "cs.os", "cs.networks", "cs.databases", 
        "cs.software.engineering", "cs.ai.ml.basics"
    ],
    "ee": [
        "math.calculus_1", "math.calculus_2", "math.calculus_3", "math.linear_algebra",
        "ee.circuits_1", "ee.circuits_2", "ee.signals_systems", "ee.control_systems",
        "ee.em_1", "ee.digital_logic", "ee.embedded"
    ],
    "physics": [
        "math.calculus_1", "math.calculus_2", "math.calculus_3", "math.linear_algebra",
        "phys.mechanics", "phys.em_intro", "phys.modern", "phys.thermo",
        "phys.quantum_1", "phys.stat_mech"
    ],
    "data-science": [
        "prog.python.basics", "math.statistics", "math.linear_algebra",
        "data.analysis", "data.visualization", "cs.ai.ml.basics",
        "data.engineering"
    ],
    "public_health": [
        "ph.epidemiology.basics", "ph.biostats.basics", "ph.env_health", 
        "ph.health_policy", "ph.global_health", "ph.program_eval"
    ],
    "materials": [
        "mat.solid_state_basics", "mat.thermo_phase", "mat.crystallography",
        "mat.polymers", "mat.ceramics", "mat.characterization"
    ]
}

# Request/Response models
class PlanRequest(BaseModel):
    major: Optional[str] = Field(None, description="Academic major: cs, ee, physics, data-science")
    goal: Optional[str] = Field(None, description="Career goal: ml-engineer, data-engineer, etc.")
    target_skills: Optional[List[str]] = Field(None, description="Custom target skills")
    baseline_mastered: List[str] = Field(default_factory=list, description="Already mastered skills")
    horizon_months: int = Field(12, description="Time horizon in months")
    weekly_hours: int = Field(15, description="Weekly study hours")
    budget: int = Field(200, description="Monthly budget in USD")
    learning_style: str = Field("mixed", description="visual, reading, hands-on, mixed")

class RoadmapStep(BaseModel):
    skill_id: str
    skill_name: str
    resources: List[Dict[str, Any]]
    est_hours: int
    start_week: int
    end_week: int
    prerequisites: List[str]
    module_id: Optional[str] = None

class Milestone(BaseModel):
    week: int
    name: str
    type: str
    description: str

class Roadmap(BaseModel):
    sequence: List[RoadmapStep]
    milestones: List[Milestone]
    summary: Dict[str, Any]
    skill_graph: Dict[str, Any]
    estimated_completion: str

# Initialize FastAPI app
app = FastAPI(
    title="AI Path Advisor API",
    description="Personalized learning roadmap generator",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Helper functions
def expand_prereqs(targets: List[str]) -> List[str]:
    """Expand target skills to include all prerequisites"""
    seen: Set[str] = set()
    order: List[str] = []
    
    def dfs(sid: str):
        if sid in seen or sid not in SKILLS:
            return
        seen.add(sid)
        for prereq in SKILLS[sid].get("prereq_ids", []):
            dfs(prereq)
        order.append(sid)
    
    for target in targets:
        dfs(target)
    
    # Return in learning order (prerequisites first)
    return order

def pick_resources(skill_id: str, budget_remain: int, target_hours: int, style: str) -> tuple:
    """Select best resources for a skill based on constraints"""
    pool = RES_BY_SKILL.get(skill_id, [])
    
    # Score resources
    scored = []
    for r in pool:
        score = r["quality_score"] * 10
        
        # Adjust for cost
        cost = 0 if r["cost"] == "free" else 50
        if cost > budget_remain:
            score -= 30
        elif r["cost"] == "free":
            score += 10
        
        # Adjust for learning style
        if style == "visual" and "video" in r["format"]:
            score += 15
        elif style == "reading" and "text" in r["format"]:
            score += 15
        elif style == "hands-on" and any(x in r["format"] for x in ["projects", "labs", "practice"]):
            score += 15
        
        # Prefer comprehensive resources
        if r["time_est_hours"] >= target_hours * 0.8:
            score += 10
        
        scored.append((score, r, cost))
    
    # Sort by score
    scored.sort(key=lambda x: -x[0])
    
    # Select top resources within budget
    chosen = []
    total_cost = 0
    total_hours = 0
    
    for score, resource, cost in scored:
        if total_cost + cost <= budget_remain or not chosen:
            chosen.append(resource)
            total_cost += cost
            total_hours += resource["time_est_hours"]
            if total_hours >= target_hours:
                break
    
    return chosen, total_cost, max(total_hours, 40)

def find_module_for_skill(skill_id: str) -> Optional[str]:
    """Find module containing this skill"""
    for module in MODULES:
        if skill_id in module["skill_ids"]:
            return module["module_id"]
    return None

def estimate_skill_hours(skill_id: str) -> int:
    """Estimate hours needed for a skill"""
    # Check if skill is in any module
    for module in MODULES:
        if skill_id in module["skill_ids"]:
            return module["target_hours"] // len(module["skill_ids"])
    
    # Default based on difficulty
    difficulty = SKILLS.get(skill_id, {}).get("difficulty", 3)
    return difficulty * 25

# API Endpoints
@app.get("/")
def root():
    return {
        "name": "AI Path Advisor API",
        "version": "1.0.0",
        "endpoints": ["/plan", "/skills", "/resources", "/modules", "/careers"]
    }

@app.get("/skills")
def get_skills():
    """Get all available skills"""
    return list(SKILLS.values())

@app.get("/resources")
def get_resources():
    """Get all available resources"""
    return RESOURCES

@app.get("/modules")
def get_modules():
    """Get all available modules"""
    return MODULES

@app.get("/careers")
def get_careers():
    """Get all career paths"""
    return CAREER_PATHS

@app.post("/plan", response_model=Roadmap)
def generate_plan(req: PlanRequest):
    """Generate a personalized learning roadmap"""
    
    # Determine target skills
    targets = []
    if req.target_skills:
        targets = req.target_skills
    elif req.goal and req.goal in CAREER_PATHS:
        targets = CAREER_PATHS[req.goal]["target_skills"]
    elif req.major and req.major in MAJOR_TARGETS:
        targets = MAJOR_TARGETS[req.major]
    else:
        raise HTTPException(400, "Must specify either major, goal, or target_skills")
    
    # Expand prerequisites
    ordered_skills = expand_prereqs(targets)
    
    # Filter out already mastered
    needed = [s for s in ordered_skills if s not in req.baseline_mastered]
    
    if not needed:
        return Roadmap(
            sequence=[],
            milestones=[],
            summary={"message": "All target skills already mastered!"},
            skill_graph={},
            estimated_completion="Already complete"
        )
    
    # Calculate budget
    monthly_budget = req.budget
    total_months = req.horizon_months
    total_budget = monthly_budget * total_months
    budget_per_skill = total_budget // len(needed) if needed else 0
    
    # Build learning sequence
    steps = []
    current_week = 1
    budget_used = 0
    
    for skill_id in needed:
        if skill_id not in SKILLS:
            continue
        
        skill = SKILLS[skill_id]
        target_hours = estimate_skill_hours(skill_id)
        
        # Pick resources
        resources, cost, hours = pick_resources(
            skill_id, 
            min(budget_per_skill, total_budget - budget_used),
            target_hours,
            req.learning_style
        )
        
        budget_used += cost
        
        # Calculate duration
        weeks_needed = max(1, math.ceil(hours / req.weekly_hours))
        
        # Create step
        step = RoadmapStep(
            skill_id=skill_id,
            skill_name=skill["name"],
            resources=resources,
            est_hours=hours,
            start_week=current_week,
            end_week=current_week + weeks_needed - 1,
            prerequisites=skill.get("prereq_ids", []),
            module_id=find_module_for_skill(skill_id)
        )
        steps.append(step)
        current_week += weeks_needed
    
    # Generate milestones
    milestones = [
        Milestone(
            week=1,
            name="Kickoff",
            type="start",
            description="Begin your learning journey"
        )
    ]
    
    # Add skill completion milestones
    for i, step in enumerate(steps):
        if (i + 1) % 3 == 0:  # Every 3 skills
            milestones.append(Milestone(
                week=step.end_week,
                name=f"Checkpoint {(i + 1) // 3}",
                type="assessment",
                description=f"Skills assessment after {i + 1} skills"
            ))
    
    # Add final milestone
    if steps:
        milestones.append(Milestone(
            week=steps[-1].end_week + 1,
            name="Capstone Project",
            type="project",
            description="Build portfolio project showcasing all skills"
        ))
    
    # Calculate completion date
    total_weeks = steps[-1].end_week if steps else 0
    completion_date = datetime.now() + timedelta(weeks=total_weeks)
    
    # Build skill graph for visualization
    skill_graph = {
        "nodes": [{"id": s.skill_id, "name": s.skill_name} for s in steps],
        "edges": []
    }
    
    for step in steps:
        for prereq in step.prerequisites:
            if any(s.skill_id == prereq for s in steps):
                skill_graph["edges"].append({"from": prereq, "to": step.skill_id})
    
    return Roadmap(
        sequence=steps,
        milestones=milestones,
        summary={
            "total_skills": len(steps),
            "total_weeks": total_weeks,
            "total_hours": sum(s.est_hours for s in steps),
            "budget_used": budget_used,
            "budget_remaining": total_budget - budget_used,
            "weekly_hours": req.weekly_hours,
            "completion_months": round(total_weeks / 4.33, 1)
        },
        skill_graph=skill_graph,
        estimated_completion=completion_date.strftime("%B %Y")
    )


# ---- Quiz System ----
QUIZ_BANK = {
    "cs": [
        {"skill": "cs.ds.algorithms",
         "q": "What is the time complexity of binary search on a sorted array of size n?",
         "choices": ["O(n)", "O(log n)", "O(n log n)", "O(1)"], "answer": 1},
        {"skill": "cs.os",
         "q": "Which component is responsible for CPU scheduling?",
         "choices": ["Filesystem", "Shell", "Kernel", "Loader"], "answer": 2},
        {"skill": "cs.databases",
         "q": "In relational databases, a foreign key enforces:",
         "choices": ["Sorting", "Referential integrity", "Normalization", "Transactions"], "answer": 1},
        {"skill": "prog.python.basics",
         "q": "In Python, which data structure is mutable?",
         "choices": ["tuple", "string", "list", "frozenset"], "answer": 2},
        {"skill": "cs.ai.ml.basics",
         "q": "In supervised learning, the training data includes:",
         "choices": ["Only features", "Only labels", "Features and labels", "Neither"], "answer": 2}
    ],
    "ee": [
        {"skill": "ee.circuits_1",
         "q": "Ohm's law relates voltage V, current I, and resistance R as:",
         "choices": ["V = I/R", "I = VR", "V = IR", "R = VI"], "answer": 2},
        {"skill": "ee.signals_systems",
         "q": "The Fourier transform maps a time-domain signal to:",
         "choices": ["z-domain", "frequency domain", "s-domain", "spatial domain"], "answer": 1},
        {"skill": "ee.control_systems",
         "q": "A negative feedback loop typically:",
         "choices": ["Destabilizes the system", "Improves stability", "Eliminates dynamics", "Adds noise"], "answer": 1},
        {"skill": "ee.digital_logic",
         "q": "A flip-flop is a:",
         "choices": ["Combinational circuit", "Sequential circuit", "Analog circuit", "Power circuit"], "answer": 1},
        {"skill": "ee.em_1",
         "q": "Maxwell's equations describe the relationship between:",
         "choices": ["Mass and energy", "Electric and magnetic fields", "Force and acceleration", "Power and resistance"], "answer": 1}
    ],
    "physics": [
        {"skill": "phys.mechanics",
         "q": "For constant mass m, Newton's second law is:",
         "choices": ["F = mv", "F = ma", "F = md", "F = m/a"], "answer": 1},
        {"skill": "phys.em_intro",
         "q": "Gauss's law relates electric flux to:",
         "choices": ["Enclosed charge", "Magnetic flux", "Current density", "Electric potential"], "answer": 0},
        {"skill": "phys.quantum_1",
         "q": "The time-independent Schrödinger equation is an eigenvalue problem for:",
         "choices": ["Momentum operator", "Hamiltonian", "Position operator", "Angular momentum"], "answer": 1},
        {"skill": "phys.thermo",
         "q": "The second law of thermodynamics states that entropy:",
         "choices": ["Always decreases", "Always increases in isolated systems", "Remains constant", "Is undefined"], "answer": 1},
        {"skill": "phys.stat_mech",
         "q": "The partition function in statistical mechanics is used to calculate:",
         "choices": ["Only energy", "Only entropy", "Thermodynamic properties", "Only temperature"], "answer": 2}
    ],
    "data-science": [
        {"skill": "data.analysis",
         "q": "Which pandas method is used to handle missing values?",
         "choices": ["dropna()", "remove_null()", "delete_missing()", "clean()"], "answer": 0},
        {"skill": "data.visualization",
         "q": "Which library is commonly used for statistical data visualization in Python?",
         "choices": ["pygame", "seaborn", "tkinter", "flask"], "answer": 1},
        {"skill": "math.statistics",
         "q": "The Central Limit Theorem states that sample means approach a:",
         "choices": ["Uniform distribution", "Normal distribution", "Exponential distribution", "Poisson distribution"], "answer": 1}
    ],
    "public_health": [
        {"skill": "ph.epidemiology.basics",
         "q": "Incidence rate measures:",
         "choices": ["Existing cases at a point in time", "New cases over a period", "Deaths only", "Exposure prevalence"], "answer": 1},
        {"skill": "ph.biostats.basics",
         "q": "A p-value is the probability of:",
         "choices": ["Null hypothesis being true", "Observing data at least as extreme if null is true", "Type II error", "Effect size"], "answer": 1},
        {"skill": "ph.program_eval",
         "q": "A randomized controlled trial primarily addresses:",
         "choices": ["External validity", "Confounding", "Measurement error", "Reporting bias"], "answer": 1},
        {"skill": "ph.health_policy",
         "q": "Health equity refers to:",
         "choices": ["Equal healthcare for all", "Fair opportunity for health", "Same health outcomes", "Free healthcare"], "answer": 1},
        {"skill": "ph.global_health",
         "q": "DALYs (Disability-Adjusted Life Years) measure:",
         "choices": ["Only mortality", "Only morbidity", "Disease burden", "Healthcare costs"], "answer": 2}
    ],
    "materials": [
        {"skill": "mat.crystallography",
         "q": "Miller indices (hkl) describe:",
         "choices": ["Defect densities", "Crystal directions", "Crystal planes", "Grain size"], "answer": 2},
        {"skill": "mat.thermo_phase",
         "q": "A eutectic point in a binary phase diagram is where:",
         "choices": ["One solid phase exists", "Liquid transforms to two solids", "No phase change occurs", "Gas phase appears"], "answer": 1},
        {"skill": "mat.solid_state_basics",
         "q": "In a semiconductor, the band gap is the energy difference between:",
         "choices": ["Two valence bands", "Valence and conduction bands", "Two conduction bands", "Fermi levels"], "answer": 1},
        {"skill": "mat.polymers",
         "q": "Cross-linking in polymers typically increases:",
         "choices": ["Flexibility", "Solubility", "Mechanical strength", "Transparency"], "answer": 2},
        {"skill": "mat.characterization",
         "q": "X-ray diffraction (XRD) is primarily used to determine:",
         "choices": ["Chemical composition", "Crystal structure", "Electrical properties", "Optical properties"], "answer": 1}
    ]
}

class QuizStartRequest(BaseModel):
    major: str = Field(..., description="Major to quiz on")
    num_items: int = Field(5, description="Number of quiz items")

class QuizItem(BaseModel):
    idx: int
    question: str
    choices: List[str]
    skill: str

class QuizStartResponse(BaseModel):
    quiz_id: str
    items: List[QuizItem]

class QuizGradeRequest(BaseModel):
    major: str
    answers: Dict[str, int]  # idx as string -> choice index

class QuizGradeResponse(BaseModel):
    score: int
    total: int
    percentage: float
    inferred_mastered: List[str]
    feedback: Dict[str, str]

@app.post("/quiz/start", response_model=QuizStartResponse)
def quiz_start(req: QuizStartRequest):
    """Start a baseline quiz for skill assessment"""
    import random
    import uuid
    
    bank = QUIZ_BANK.get(req.major, [])
    if not bank:
        raise HTTPException(400, f"No quiz available for major: {req.major}")
    
    # Select random questions
    selected = random.sample(bank, min(req.num_items, len(bank)))
    items = [
        QuizItem(
            idx=i, 
            question=q["q"], 
            choices=q["choices"],
            skill=q["skill"]
        ) 
        for i, q in enumerate(selected)
    ]
    
    return QuizStartResponse(
        quiz_id=str(uuid.uuid4()),
        items=items
    )

@app.post("/quiz/grade", response_model=QuizGradeResponse)
def quiz_grade(req: QuizGradeRequest):
    """Grade quiz and infer mastered skills"""
    bank = QUIZ_BANK.get(req.major, [])
    if not bank:
        raise HTTPException(400, f"No quiz available for major: {req.major}")
    
    score = 0
    mastered = []
    feedback = {}
    
    # Grade each answer
    for idx_str, answer in req.answers.items():
        idx = int(idx_str)
        if idx < len(bank):
            question = bank[idx]
            correct = question["answer"]
            if answer == correct:
                score += 1
                mastered.append(question["skill"])
                feedback[idx_str] = "Correct!"
            else:
                feedback[idx_str] = f"Incorrect. The correct answer was: {question['choices'][correct]}"
    
    total = len(req.answers)
    percentage = (score / total * 100) if total > 0 else 0
    
    # Remove duplicates from mastered skills
    mastered = list(set(mastered))
    
    return QuizGradeResponse(
        score=score,
        total=total,
        percentage=round(percentage, 1),
        inferred_mastered=mastered,
        feedback=feedback
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
