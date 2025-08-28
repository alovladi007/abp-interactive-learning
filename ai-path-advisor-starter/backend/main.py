
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
