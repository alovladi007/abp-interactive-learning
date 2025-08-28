"""
AI Path Advisor Pro - Advanced Backend with ILP Optimization
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional, Set
import json, os, math
from datetime import datetime, timedelta

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

def load_json(name: str):
    with open(os.path.join(DATA_DIR, name), "r") as f:
        return json.load(f)

SKILLS = {s["skill_id"]: s for s in load_json("skills.json")}
MODULES = load_json("modules.json")
RESOURCES = load_json("resources.json")
ROLES = load_json("roles.json")

# Build resource index by skill
RES_BY_SKILL: Dict[str, List[Dict[str, Any]]] = {}
for r in RESOURCES:
    for sid in r["skills"]:
        RES_BY_SKILL.setdefault(sid, []).append(r)

# Major to target skills mapping
MAJOR_TARGETS = {
    "cs":[
        "prog.python.basics","prog.c.basics","math.discrete","cs.ds.algorithms",
        "cs.computer.arch","cs.os","cs.networks","cs.databases","cs.software.engineering"
    ],
    "ee":[
        "math.calculus_1","math.calculus_2","math.calculus_3","math.linear_algebra",
        "ee.circuits_1","ee.circuits_2","ee.signals_systems","ee.control_systems",
        "ee.em_1","ee.comm_systems","ee.digital_logic","ee.semiconductor_devices"
    ],
    "physics":[
        "math.calculus_1","math.calculus_2","math.calculus_3","math.linear_algebra",
        "phys.mechanics","phys.em_intro","phys.modern","phys.thermo","phys.quantum_1",
        "phys.em_advanced","phys.stat_mech"
    ],
    "public_health":[
        "ph.epidemiology.basics","ph.biostats.basics","ph.env_health","ph.health_policy","ph.global_health","ph.program_eval"
    ],
    "materials":[
        "mat.solid_state_basics","mat.thermo_phase","mat.crystallography","mat.polymers","mat.ceramics","mat.characterization"
    ],
    "medicine":[
        "med.anatomy","med.physiology","med.biochem","med.micro","med.pathology","med.pharmacology"
    ],
    "nursing":[
        "nurse.anatomy","nurse.pathophys","nurse.pharm","nurse.clinical"
    ],
    "pharmacy":[
        "pharm.medicinal_chem","pharm.pharmacology","pharm.pharmacokinetics","pharm.toxicology"
    ],
    "nutrition":[
        "nutr.biochem","nutr.food_science","nutr.clinical"
    ],
    "me":[
        "me.statics","me.dynamics","me.thermo","me.fluids","me.heat_transfer","me.machine_design"
    ],
    "civil":[
        "ce.structural","ce.soils","ce.hydrology","ce.transport","ce.concrete","ce.steel"
    ],
    "chemeng":[
        "che.meb","che.thermo","che.transport","che.kinetics","che.control"
    ],
    "environment":[
        "env.chem","env.air","env.water","env.climate"
    ],
    "bme":[
        "bme.bio","bme.biomech","bme.imaging","bme.tissue","bme.bioinstr"
    ],
    "law":[
        "law.contracts","law.torts","law.criminal","law.constitutional","law.civpro","law.legal_writing"
    ],
    "policy":[
        "pp.comparative","pp.ir","pp.theory","pp.policy_analysis","pp.methods"
    ],
    "economics":[
        "econ.micro","econ.macro","econ.econometrics","econ.timeseries"
    ],
    "education":[
        "edu.learning","edu.curriculum","edu.assessment","edu.edtech"
    ],
    "architecture":[
        "arch.design","arch.materials","arch.sustainability","arch.urban","arch.codes"
    ],
    "communications":[
        "comm.writing","comm.media_law","comm.investigative","comm.data_journalism"
    ]
}

# Quiz bank for baseline assessment
QUIZ_BANK = {
    "cs": [
        {"skill":"cs.ds.algorithms","q":"Binary search on a sorted array of size n has complexity:","choices":["O(n)","O(log n)","O(n log n)","O(1)"], "answer":1},
        {"skill":"cs.os","q":"Which component schedules the CPU?","choices":["Filesystem","Shell","Kernel","Loader"], "answer":2},
        {"skill":"cs.databases","q":"A foreign key enforces:","choices":["Sorting","Referential integrity","Normalization","Transactions"], "answer":1}
    ],
    "ee": [
        {"skill":"ee.circuits_1","q":"Ohm's law:","choices":["v=i/R","i=vR","v=iR","R=vi"], "answer":2},
        {"skill":"ee.signals_systems","q":"Fourier transform maps to:","choices":["z-domain","frequency-domain","time-frequency only","s-domain"], "answer":1},
        {"skill":"ee.control_systems","q":"Negative feedback typically:","choices":["destabilizes","improves robustness","eliminates dynamics","adds noise"], "answer":1}
    ],
    "physics": [
        {"skill":"phys.mechanics","q":"Newton's second law:","choices":["F=mv","F=ma","F=md","F=∫m dt"], "answer":1},
        {"skill":"phys.em_intro","q":"Gauss's law relates electric flux to:","choices":["charge density","magnetic flux","current density","electric potential"], "answer":0},
        {"skill":"phys.quantum_1","q":"Time-independent Schrödinger equation is eigenvalue problem for:","choices":["momentum","Hamiltonian","position","angular momentum"], "answer":1}
    ],
    "public_health": [
        {"skill":"ph.epidemiology.basics","q":"Incidence rate measures:","choices":["Existing cases","New cases over time","Fatalities only","Exposure prevalence"], "answer":1},
        {"skill":"ph.biostats.basics","q":"A p-value is probability of:","choices":["null true","data at least as extreme given null","FDR","type II error"], "answer":1},
        {"skill":"ph.program_eval","q":"RCTs primarily address:","choices":["External validity","Confounding","Measurement error","Selection bias only"], "answer":1}
    ],
    "materials": [
        {"skill":"mat.crystallography","q":"Miller indices (hkl) describe:","choices":["defect densities","slip systems","crystal planes","grain size"], "answer":2},
        {"skill":"mat.thermo_phase","q":"Eutectic point is where:","choices":["both solid","liquid→two solids at single comp & temp","no phase change","only peritectic"], "answer":1},
        {"skill":"mat.solid_state_basics","q":"Intrinsic semiconductor Fermi level lies:","choices":["near valence","near conduction","mid-gap","outside gap"], "answer":2}
    ]
}

app = FastAPI(title="AI Path Advisor Pro - Backend")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic Models
class PlanRequest(BaseModel):
    major: Optional[str] = Field(None, description="Major or None if using role")
    role: Optional[str] = Field(None, description="Career path key from roles.json")
    target_skills: Optional[List[str]] = None
    baseline_mastered: List[str] = []
    horizon_months: int = 10
    weekly_hours: int = 10
    budget: int = 100
    # weights
    w_time: float = 1.0
    w_cost: float = 0.5
    w_quality: float = 1.0
    w_difficulty: float = 0.1
    # preferences
    prefer_formats: List[str] = []
    variant: Optional[str] = Field(None, description="'balanced'|'fastest'|'cheapest'")

class RoadmapStep(BaseModel):
    skill_id: str
    resources: List[str]
    est_hours: int
    start_week: int
    end_week: int

class Roadmap(BaseModel):
    sequence: List[RoadmapStep]
    milestones: List[Dict[str, Any]]
    summary: Dict[str, Any]

class QuizStartRequest(BaseModel):
    major: str
    num_items: int = 3

class QuizItem(BaseModel):
    idx: int
    question: str
    choices: List[str]

class QuizStartResponse(BaseModel):
    items: List[QuizItem]

class QuizGradeRequest(BaseModel):
    major: str
    answers: Dict[int, int]

class QuizGradeResponse(BaseModel):
    score: int
    total: int
    inferred_mastered: List[str]

# Helper functions
def expand_prereqs(targets: List[str]) -> List[str]:
    """Expand target skills to include all prerequisites"""
    seen: Set[str] = set()
    order: List[str] = []
    
    def dfs(sid: str):
        if sid in seen: return
        seen.add(sid)
        for p in SKILLS.get(sid, {}).get("prereq_ids", []):
            dfs(p)
        order.append(sid)
    
    for t in targets:
        dfs(t)
    
    out = []
    for sid in order:
        if sid not in out: out.append(sid)
    return out

def module_hours_for_skill(sid: str) -> int:
    """Estimate hours for a skill based on modules"""
    hours = []
    for m in MODULES:
        if sid in m["skill_ids"]:
            hours.append(int(m.get("target_hours", 60) / len(m["skill_ids"])))
    return int(sum(hours)/len(hours)) if hours else 60

def resource_price(r: Dict[str, Any]) -> int:
    """Estimate resource price"""
    if "price_est" in r: return int(r["price_est"])
    return 0 if r.get("cost","free") == "free" else 50

def personalized_penalty(r: Dict[str, Any], prefer_formats: List[str]) -> float:
    """Apply penalty based on format preferences"""
    if not prefer_formats: return 0.0
    fmts = set([f.lower() for f in r.get("format", [])])
    prefer = set([p.lower() for p in prefer_formats])
    match = len(fmts & prefer)
    return -0.2 * match

def optimize_resources_for_skills(skills_needed: List[str], budget: int, weights: Dict[str, float], prefer_formats: List[str]) -> Dict[str, Dict[str, Any]]:
    """Use ILP to optimize resource selection"""
    try:
        import pulp
        
        # Create optimization problem
        prob = pulp.LpProblem("resource_selection", pulp.LpMinimize)
        x = {}
        costs = []
        
        # Create decision variables for each resource option
        for sid in skills_needed:
            pool = RES_BY_SKILL.get(sid, [])
            for i, r in enumerate(pool):
                var = pulp.LpVariable(f"x_{sid}_{i}", lowBound=0, upBound=1, cat="Binary")
                x[(sid, i)] = var
                
                # Calculate penalty
                time = float(r.get("time_est_hours", 60))
                price = float(resource_price(r))
                quality = float(r.get("quality_score", 8.0))
                diff = float(SKILLS[sid].get("difficulty", 3))
                pref = personalized_penalty(r, prefer_formats)
                
                penalty = weights["w_time"]*time + weights["w_cost"]*price - weights["w_quality"]*quality + weights["w_difficulty"]*diff + pref
                costs.append(penalty * var)
            
            # Constraint: exactly one resource per skill
            if pool:
                prob += pulp.lpSum([x[(sid, i)] for i, _ in enumerate(pool)]) == 1
        
        # Budget constraint
        prob += pulp.lpSum([resource_price(RES_BY_SKILL[sid][i]) * x[(sid, i)]
                            for sid in skills_needed for i,_ in enumerate(RES_BY_SKILL.get(sid, []))]) <= budget
        
        # Objective: minimize total penalty
        prob += pulp.lpSum(costs)
        
        # Solve
        prob.solve(pulp.PULP_CBC_CMD(msg=False))
        
        # Extract solution
        chosen = {}
        for sid in skills_needed:
            pool = RES_BY_SKILL.get(sid, [])
            if not pool: continue
            
            pick = None
            for i, r in enumerate(pool):
                var = x[(sid, i)]
                if var.value() and var.value() > 0.5:
                    pick = r
                    break
            
            if pick is None:
                pick = pool[0]  # Fallback to first option
            chosen[sid] = pick
        
        return chosen
        
    except Exception:
        # Fallback to simple heuristic
        chosen = {}
        for sid in skills_needed:
            pool = RES_BY_SKILL.get(sid, [])
            pool = sorted(pool, key=lambda r: (r["time_est_hours"], -r["quality_score"], r["cost"]!="free"))
            if pool:
                chosen[sid] = pool[0]
        return chosen

def planned_hours_for_skill(sid: str, chosen_resource: Dict[str, Any]) -> int:
    """Calculate planned hours for a skill"""
    est = module_hours_for_skill(sid)
    r_hours = int(chosen_resource.get("time_est_hours", 60)) if chosen_resource else 0
    return max(est, r_hours)

def apply_variant_weights(req: PlanRequest):
    """Apply preset weight variants"""
    if req.variant == "fastest":
        req.w_time, req.w_cost, req.w_quality = 1.5, 0.2, 1.0
    elif req.variant == "cheapest":
        req.w_time, req.w_cost, req.w_quality = 1.0, 2.0, 0.8

# API Endpoints
@app.get("/")
def root():
    return {
        "name": "AI Path Advisor Pro",
        "version": "2.0.0",
        "features": [
            "ILP resource optimization",
            "20 majors support",
            "Career role planning",
            "Baseline quiz system",
            "Progress tracking",
            "ICS calendar export",
            "Capstone generation"
        ]
    }

@app.get("/majors")
def list_majors():
    return list(MAJOR_TARGETS.keys())

@app.get("/roles")
def list_roles():
    return [{"key":k, "name":v["name"], "skills":v["skills"]} for k,v in ROLES.items()]

@app.post("/plan", response_model=Roadmap)
def plan(req: PlanRequest):
    """Generate optimized learning roadmap"""
    # Determine target skills
    if req.role:
        targets = ROLES.get(req.role, {}).get("skills", [])
        if not targets:
            raise HTTPException(status_code=400, detail=f"Unknown role: {req.role}")
    else:
        if not req.major:
            raise HTTPException(status_code=400, detail="Provide either 'role' or 'major'")
        if req.major not in MAJOR_TARGETS:
            raise HTTPException(status_code=400, detail=f"Unknown major: {req.major}")
        targets = req.target_skills or MAJOR_TARGETS[req.major]
    
    # Apply variant weights
    apply_variant_weights(req)
    
    # Expand prerequisites
    ordered = expand_prereqs(targets)
    ordered = [sid for sid in ordered if sid in SKILLS]
    
    # Filter out already mastered
    needed = [sid for sid in ordered if sid not in set(req.baseline_mastered)]
    
    # Optimize resource selection
    weights = dict(w_time=req.w_time, w_cost=req.w_cost, w_quality=req.w_quality, w_difficulty=req.w_difficulty)
    choice = optimize_resources_for_skills(needed, req.budget, weights, req.prefer_formats)
    
    # Build roadmap
    steps: List[RoadmapStep] = []
    week = 1
    weekly_hours = max(1, req.weekly_hours)
    diagnostics = []
    budget_left = req.budget - sum(resource_price(choice.get(sid, {})) for sid in needed)
    
    for sid in needed:
        res = choice.get(sid)
        hours = planned_hours_for_skill(sid, res)
        duration_weeks = max(1, math.ceil(hours / weekly_hours))
        
        step = RoadmapStep(
            skill_id=sid,
            resources=[res["resource_id"]] if res else [],
            est_hours=hours,
            start_week=week,
            end_week=week+duration_weeks-1
        )
        steps.append(step)
        
        # Add diagnostic every 2 weeks
        if (step.end_week // 2) > (step.start_week // 2):
            diagnostics.append({"week": step.end_week, "type": "diagnostic", "skill": sid})
        
        week += duration_weeks
    
    total_weeks = steps[-1].end_week if steps else 0
    
    # Create milestones
    milestones = [{"name":"Kickoff","week":1}]
    milestones.extend([{"name":"Diagnostic", **d} for d in diagnostics])
    milestones.append({"name":"Capstone (publish portfolio)","week":total_weeks})
    
    return Roadmap(
        sequence=steps,
        milestones=milestones,
        summary={
            "role": req.role,
            "major": req.major,
            "target_skills": targets,
            "weeks_total": total_weeks,
            "budget_left": int(budget_left),
            "weekly_hours": weekly_hours,
            "weights": weights,
            "preferences": req.prefer_formats
        }
    )

@app.post("/quiz/start", response_model=QuizStartResponse)
def quiz_start(req: QuizStartRequest):
    """Start a baseline assessment quiz"""
    bank = QUIZ_BANK.get(req.major, [])[:req.num_items]
    items = [QuizItem(idx=i, question=q["q"], choices=q["choices"]) for i, q in enumerate(bank)]
    return QuizStartResponse(items=items)

@app.post("/quiz/grade", response_model=QuizGradeResponse)
def quiz_grade(req: QuizGradeRequest):
    """Grade quiz and infer mastered skills"""
    bank = QUIZ_BANK.get(req.major, [])
    score = 0
    mastered = []
    
    for i, q in enumerate(bank[:len(req.answers)]):
        ans = req.answers.get(str(i), -1)  # Convert key to string
        if ans == q["answer"]:
            score += 1
            mastered.append(q["skill"])
    
    return QuizGradeResponse(score=score, total=len(req.answers), inferred_mastered=mastered)

# Progress persistence
PROGRESS_PATH = os.path.join(DATA_DIR, "progress.json")

@app.post("/progress/save")
def progress_save(payload: Dict[str, Any]):
    """Save progress data"""
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(PROGRESS_PATH, "w") as f:
        json.dump(payload, f)
    return {"ok": True}

@app.get("/progress/load")
def progress_load():
    """Load progress data"""
    if not os.path.exists(PROGRESS_PATH):
        return {"ok": False, "data": {}}
    with open(PROGRESS_PATH, "r") as f:
        return {"ok": True, "data": json.load(f)}

@app.get("/export/ics", response_class=PlainTextResponse)
def export_ics(major: Optional[str] = None, role: Optional[str] = None, weekly_hours: int = 10):
    """Export roadmap as ICS calendar file"""
    now = datetime.utcnow().date()
    lines = ["BEGIN:VCALENDAR","VERSION:2.0","PRODID:-//AI Path Advisor Pro//EN"]
    
    for w in range(1,13):
        dt = now + timedelta(days=(w-1)*7)
        lines += [
            "BEGIN:VEVENT",
            f"UID:study-week-{w}@ai-path-advisor",
            f"DTSTART;VALUE=DATE:{dt.strftime('%Y%m%d')}",
            f"SUMMARY:Study Week {w} - {role or major or 'Roadmap'}",
            f"DESCRIPTION:{weekly_hours} planned hours",
            "END:VEVENT"
        ]
    
    lines.append("END:VCALENDAR")
    return "\n".join(lines)

@app.post("/capstone")
def capstone(payload: Dict[str, Any]):
    """Generate capstone project specification"""
    skills_done = payload.get("skills_done", [])
    
    # Determine theme based on skills
    theme = "systems" if any(s.startswith("cs.") for s in skills_done) else \
            "devices" if any(s.startswith("ee.") for s in skills_done) else \
            "analysis"
    
    spec = {
        "title": f"Capstone — {theme.title()} Project",
        "objectives": [
            "Integrate 3+ core skills",
            "Include tests/metrics",
            "Public artifact (repo/report/demo)"
        ],
        "deliverables": [
            "Design doc (2–4 pages)",
            "MVP with tests and README",
            "Evaluation results with metrics",
            "Video walkthrough (5–10 min)"
        ],
        "rubric": [
            {"criterion":"Technical depth","weight":0.35},
            {"criterion":"Rigor & evaluation","weight":0.25},
            {"criterion":"Clarity & documentation","weight":0.20},
            {"criterion":"UX/Polish","weight":0.10},
            {"criterion":"Originality","weight":0.10}
        ]
    }
    return spec

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)