#!/usr/bin/env python3
"""
Extends AI Path Advisor with:
- Public Health and Materials Science majors
- Baseline skills quiz system
- Frontend quiz UI integration
"""

import os
import json
import re
import shutil

root = "/workspace/ai-path-advisor-starter"
backend = os.path.join(root, "backend")
frontend = os.path.join(root, "frontend")
data_dir = os.path.join(backend, "data")

# ---------- Load existing JSONs ----------
print("Loading existing data files...")
with open(os.path.join(data_dir, "skills.json"), "r") as f:
    skills = json.load(f)
with open(os.path.join(data_dir, "modules.json"), "r") as f:
    modules = json.load(f)
with open(os.path.join(data_dir, "resources.json"), "r") as f:
    resources = json.load(f)

skill_ids = {s["skill_id"] for s in skills}

# ---------- Add new skills for Public Health and Materials Science ----------
print("Adding Public Health and Materials Science skills...")
new_skills = [
    # Public Health
    {"skill_id":"ph.epidemiology.basics","name":"Epidemiology Basics","prereq_ids":[],"tags":["public_health"],"difficulty":2},
    {"skill_id":"ph.biostats.basics","name":"Biostatistics Basics","prereq_ids":["math.statistics"],"tags":["public_health","stats"],"difficulty":3},
    {"skill_id":"ph.health_policy","name":"Health Policy & Systems","prereq_ids":[],"tags":["public_health","policy"],"difficulty":2},
    {"skill_id":"ph.env_health","name":"Environmental Health","prereq_ids":[],"tags":["public_health"],"difficulty":2},
    {"skill_id":"ph.global_health","name":"Global Health","prereq_ids":["ph.epidemiology.basics"],"tags":["public_health"],"difficulty":3},
    {"skill_id":"ph.program_eval","name":"Program Evaluation","prereq_ids":["ph.biostats.basics","ph.epidemiology.basics"],"tags":["public_health"],"difficulty":3},
    {"skill_id":"ph.health_econ","name":"Health Economics","prereq_ids":["ph.health_policy"],"tags":["public_health","economics"],"difficulty":3},
    {"skill_id":"ph.infectious_disease","name":"Infectious Disease Epidemiology","prereq_ids":["ph.epidemiology.basics"],"tags":["public_health"],"difficulty":3},
    {"skill_id":"ph.chronic_disease","name":"Chronic Disease Epidemiology","prereq_ids":["ph.epidemiology.basics"],"tags":["public_health"],"difficulty":3},
    {"skill_id":"ph.health_behavior","name":"Health Behavior & Education","prereq_ids":[],"tags":["public_health"],"difficulty":2},

    # Materials Science
    {"skill_id":"mat.solid_state_basics","name":"Solid State Basics","prereq_ids":["math.calculus_2","math.linear_algebra","phys.modern"],"tags":["materials","physics"],"difficulty":3},
    {"skill_id":"mat.thermo_phase","name":"Thermodynamics & Phase Transformations","prereq_ids":["math.calculus_2","phys.thermo"],"tags":["materials"],"difficulty":3},
    {"skill_id":"mat.crystallography","name":"Crystallography & Diffraction","prereq_ids":["math.linear_algebra","phys.modern"],"tags":["materials"],"difficulty":3},
    {"skill_id":"mat.polymers","name":"Polymer Science","prereq_ids":["math.calculus_1"],"tags":["materials"],"difficulty":2},
    {"skill_id":"mat.ceramics","name":"Ceramics","prereq_ids":["mat.crystallography"],"tags":["materials"],"difficulty":3},
    {"skill_id":"mat.characterization","name":"Materials Characterization","prereq_ids":["mat.crystallography"],"tags":["materials"],"difficulty":3},
    {"skill_id":"mat.electronic_materials","name":"Electronic Materials","prereq_ids":["mat.solid_state_basics","ee.semiconductor_devices"],"tags":["materials","electronics"],"difficulty":4},
    {"skill_id":"mat.biomaterials","name":"Biomaterials","prereq_ids":["mat.polymers"],"tags":["materials","bio"],"difficulty":3},
    {"skill_id":"mat.nanomaterials","name":"Nanomaterials","prereq_ids":["mat.solid_state_basics","mat.characterization"],"tags":["materials","nano"],"difficulty":4},
    {"skill_id":"mat.computational","name":"Computational Materials Science","prereq_ids":["mat.solid_state_basics","prog.python.basics"],"tags":["materials","computational"],"difficulty":4},
]

# Remove duplicates and add new skills
existing_skill_ids = {s["skill_id"] for s in skills}
for new_skill in new_skills:
    if new_skill["skill_id"] not in existing_skill_ids:
        skills.append(new_skill)

# ---------- Add modules for new majors ----------
print("Adding new modules...")
new_modules = [
    # Public Health
    {
        "module_id":"ph.core.sequence",
        "skill_ids":["ph.epidemiology.basics","ph.biostats.basics","ph.env_health","ph.health_policy"],
        "outcomes":["Incidence/prevalence/causality","Intro biostatistics","Environmental risk assessment","Policy frameworks"],
        "assessments":["epi case analyses","R-based stats mini-labs","policy brief"],
        "project_ideas":["Design a community health intervention","Analyze public health dataset"],
        "target_hours": 140
    },
    {
        "module_id":"ph.advanced.eval",
        "skill_ids":["ph.global_health","ph.program_eval","ph.health_econ"],
        "outcomes":["Global burden metrics","Logic models, RCT vs quasi-experimental","Cost-effectiveness analysis"],
        "assessments":["program evaluation plan","economic evaluation"],
        "project_ideas":["Impact evaluation design with DAGs","QALY/DALY calculation"],
        "target_hours": 120
    },
    {
        "module_id":"ph.disease.focus",
        "skill_ids":["ph.infectious_disease","ph.chronic_disease","ph.health_behavior"],
        "outcomes":["Disease transmission models","Risk factor analysis","Behavior change theories"],
        "assessments":["outbreak investigation","cohort study design"],
        "project_ideas":["SIR model implementation","Health promotion campaign"],
        "target_hours": 100
    },

    # Materials Science
    {
        "module_id":"mat.foundations",
        "skill_ids":["mat.solid_state_basics","mat.thermo_phase","mat.crystallography"],
        "outcomes":["Band theory/defects","Phase diagrams","Lattice structures/diffraction"],
        "assessments":["problem sets","diffraction indexing exercise","phase diagram analysis"],
        "project_ideas":["Phase diagram case study","Crystal structure visualization"],
        "target_hours": 150
    },
    {
        "module_id":"mat.applications",
        "skill_ids":["mat.polymers","mat.ceramics","mat.characterization"],
        "outcomes":["Polymer properties","Ceramic processing","XRD/SEM/TEM basics"],
        "assessments":["materials selection project","characterization lab reports"],
        "project_ideas":["Materials selection for application","Characterization proposal"],
        "target_hours": 120
    },
    {
        "module_id":"mat.advanced",
        "skill_ids":["mat.electronic_materials","mat.biomaterials","mat.nanomaterials","mat.computational"],
        "outcomes":["Semiconductor materials","Biocompatibility","Nanoscale properties","DFT/MD basics"],
        "assessments":["device design","biocompatibility study","computational project"],
        "project_ideas":["Solar cell materials design","Drug delivery system","Nanoparticle synthesis","Materials simulation"],
        "target_hours": 160
    },
]

# Add new modules
existing_module_ids = {m["module_id"] for m in modules}
for new_module in new_modules:
    if new_module["module_id"] not in existing_module_ids:
        modules.append(new_module)

# ---------- Add resources for new skills ----------
print("Adding new resources...")
new_resources = [
    # Public Health Resources
    {"resource_id":"book.gordis_epi","type":"book","title":"Gordis Epidemiology","provider":"Elsevier","skills":["ph.epidemiology.basics"],"level":"intro","time_est_hours":50,"quality_score":9.0,"cost":"paid","format":["text","problems"]},
    {"resource_id":"book.rosner_biostats","type":"book","title":"Fundamentals of Biostatistics","provider":"Rosner","skills":["ph.biostats.basics"],"level":"intermediate","time_est_hours":80,"quality_score":8.8,"cost":"paid","format":["text","problems"]},
    {"resource_id":"course.r_for_epi","type":"course","title":"R for Epidemiology","provider":"Applied Epi","skills":["ph.biostats.basics","ph.epidemiology.basics"],"level":"intro","time_est_hours":40,"quality_score":8.9,"cost":"free","format":["text","labs"]},
    {"resource_id":"book.friis_envhealth","type":"book","title":"Essentials of Environmental Health","provider":"Friis","skills":["ph.env_health"],"level":"intro","time_est_hours":50,"quality_score":8.5,"cost":"paid","format":["text"]},
    {"resource_id":"book.bhattacharya_healthecon","type":"book","title":"Health Economics","provider":"Bhattacharya et al.","skills":["ph.health_econ","ph.health_policy"],"level":"intermediate","time_est_hours":70,"quality_score":8.7,"cost":"paid","format":["text","problems"]},
    {"resource_id":"course.global_burden","type":"course","title":"Global Health Metrics","provider":"IHME/GBD","skills":["ph.global_health"],"level":"intermediate","time_est_hours":40,"quality_score":8.6,"cost":"free","format":["video","data"]},
    {"resource_id":"book.rothman_modern_epi","type":"book","title":"Modern Epidemiology","provider":"Rothman et al.","skills":["ph.program_eval","ph.epidemiology.basics"],"level":"advanced","time_est_hours":120,"quality_score":9.2,"cost":"paid","format":["text","theory"]},
    {"resource_id":"course.coursera_global_health","type":"course","title":"Global Health Specialization","provider":"Coursera/Duke","skills":["ph.global_health","ph.health_policy"],"level":"intro","time_est_hours":60,"quality_score":8.7,"cost":"paid","format":["video","quizzes"]},
    {"resource_id":"book.glanz_health_behavior","type":"book","title":"Health Behavior and Health Education","provider":"Glanz et al.","skills":["ph.health_behavior"],"level":"intermediate","time_est_hours":60,"quality_score":8.8,"cost":"paid","format":["text","cases"]},

    # Materials Science Resources
    {"resource_id":"book.callister_materials","type":"book","title":"Materials Science and Engineering: An Introduction","provider":"Callister & Rethwisch","skills":["mat.thermo_phase","mat.solid_state_basics","mat.crystallography"],"level":"intro","time_est_hours":120,"quality_score":9.0,"cost":"paid","format":["text","problems"]},
    {"resource_id":"book.porter_phase","type":"book","title":"Phase Transformations in Metals and Alloys","provider":"Porter & Easterling","skills":["mat.thermo_phase"],"level":"advanced","time_est_hours":90,"quality_score":9.1,"cost":"paid","format":["text","diagrams"]},
    {"resource_id":"book.cullity_xrd","type":"book","title":"Elements of X-Ray Diffraction","provider":"Cullity & Stock","skills":["mat.crystallography","mat.characterization"],"level":"advanced","time_est_hours":80,"quality_score":9.0,"cost":"paid","format":["text","labs"]},
    {"resource_id":"book.kittel_solid","type":"book","title":"Introduction to Solid State Physics","provider":"Kittel","skills":["mat.solid_state_basics"],"level":"advanced","time_est_hours":100,"quality_score":8.8,"cost":"paid","format":["text","problems"]},
    {"resource_id":"book.kingery_ceramics","type":"book","title":"Introduction to Ceramics","provider":"Kingery et al.","skills":["mat.ceramics"],"level":"advanced","time_est_hours":90,"quality_score":8.7,"cost":"paid","format":["text"]},
    {"resource_id":"book.young_polymers","type":"book","title":"Introduction to Polymers","provider":"Young & Lovell","skills":["mat.polymers"],"level":"intermediate","time_est_hours":80,"quality_score":8.8,"cost":"paid","format":["text","problems"]},
    {"resource_id":"course.mit_3091","type":"course","title":"MIT 3.091 Introduction to Solid State Chemistry","provider":"MIT OCW","skills":["mat.solid_state_basics","mat.crystallography"],"level":"intro","time_est_hours":80,"quality_score":9.2,"cost":"free","format":["video","problems"]},
    {"resource_id":"book.ratner_biomaterials","type":"book","title":"Biomaterials Science","provider":"Ratner et al.","skills":["mat.biomaterials"],"level":"advanced","time_est_hours":100,"quality_score":9.0,"cost":"paid","format":["text","cases"]},
    {"resource_id":"book.cao_nanostructures","type":"book","title":"Nanostructures and Nanomaterials","provider":"Cao & Wang","skills":["mat.nanomaterials"],"level":"advanced","time_est_hours":90,"quality_score":8.7,"cost":"paid","format":["text"]},
    {"resource_id":"course.computational_materials","type":"course","title":"Computational Materials Science","provider":"NPTEL","skills":["mat.computational"],"level":"intermediate","time_est_hours":60,"quality_score":8.5,"cost":"free","format":["video","assignments"]},
]

# Add new resources
existing_resource_ids = {r["resource_id"] for r in resources}
for new_resource in new_resources:
    if new_resource["resource_id"] not in existing_resource_ids:
        resources.append(new_resource)

# Save updated JSONs
print("Saving updated data files...")
with open(os.path.join(data_dir, "skills.json"), "w") as f:
    json.dump(skills, f, indent=2)
with open(os.path.join(data_dir, "modules.json"), "w") as f:
    json.dump(modules, f, indent=2)
with open(os.path.join(data_dir, "resources.json"), "w") as f:
    json.dump(resources, f, indent=2)

# ---------- Update FastAPI main.py ----------
print("Updating FastAPI backend...")
main_path = os.path.join(backend, "main.py")
with open(main_path, "r") as f:
    main_py = f.read()

# Update MAJOR_TARGETS to include new majors
if '"public_health"' not in main_py:
    # Find and update MAJOR_TARGETS
    major_targets_new = '''MAJOR_TARGETS = {
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
}'''
    
    # Replace MAJOR_TARGETS
    main_py = re.sub(
        r'MAJOR_TARGETS = \{[^}]+\}',
        major_targets_new,
        main_py,
        flags=re.DOTALL
    )

# Add quiz system if not present
if "QUIZ_BANK" not in main_py:
    quiz_code = '''
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
'''
    
    # Insert quiz code before the main block
    if "__name__" in main_py:
        main_py = main_py.replace('if __name__ == "__main__":', quiz_code + '\nif __name__ == "__main__":')
    else:
        main_py += quiz_code

# Save updated main.py
with open(main_path, "w") as f:
    f.write(main_py)

# ---------- Update Frontend ----------
print("Updating frontend with quiz UI...")
page_path = os.path.join(frontend, "app", "page.tsx")
with open(page_path, "r") as f:
    page_tsx = f.read()

# Add quiz functionality if not present
if "startQuiz" not in page_tsx:
    # Find where to insert quiz state
    state_insert = """  const [error, setError] = useState<string | null>(null)
  const [quizItems, setQuizItems] = useState<any[]>([])
  const [quizAnswers, setQuizAnswers] = useState<{[key: string]: number}>({})
  const [quizResult, setQuizResult] = useState<any>(null)
  const [showQuiz, setShowQuiz] = useState(false)"""
    
    page_tsx = page_tsx.replace(
        "  const [error, setError] = useState<string | null>(null)",
        state_insert
    )
    
    # Add quiz functions before generateRoadmap
    quiz_functions = """
  const startQuiz = async () => {
    setQuizItems([])
    setQuizResult(null)
    setQuizAnswers({})
    setShowQuiz(true)
    
    try {
      const response = await axios.post(`${API_URL}/quiz/start`, {
        major: formData.major,
        num_items: 5
      })
      setQuizItems(response.data.items)
    } catch (err) {
      console.error('Failed to start quiz:', err)
      setError('Failed to load quiz')
    }
  }

  const gradeQuiz = async () => {
    try {
      const response = await axios.post(`${API_URL}/quiz/grade`, {
        major: formData.major,
        answers: quizAnswers
      })
      
      setQuizResult(response.data)
      
      // Add mastered skills to baseline
      if (response.data.inferred_mastered?.length > 0) {
        const currentSkills = formData.baseline
          .split(',')
          .map((s: string) => s.trim())
          .filter(Boolean)
        const newSkills = [...new Set([...currentSkills, ...response.data.inferred_mastered])]
        setFormData({...formData, baseline: newSkills.join(', ')})
      }
    } catch (err) {
      console.error('Failed to grade quiz:', err)
      setError('Failed to grade quiz')
    }
  }
"""
    
    # Insert functions before generateRoadmap
    page_tsx = page_tsx.replace(
        "  const generateRoadmap = async () => {",
        quiz_functions + "\n  const generateRoadmap = async () => {"
    )
    
    # Add quiz UI in the form section
    quiz_ui = """
                <div className="md:col-span-2 border-t pt-4 mt-4">
                  <h3 className="text-lg font-semibold mb-3">Skill Assessment Quiz</h3>
                  <p className="text-sm text-gray-600 dark:text-gray-400 mb-3">
                    Take a quick quiz to assess your current knowledge and automatically add mastered skills to your baseline.
                  </p>
                  
                  {!showQuiz && (
                    <button
                      type="button"
                      onClick={startQuiz}
                      className="bg-green-600 text-white py-2 px-4 rounded-md hover:bg-green-700 font-medium"
                    >
                      Take Baseline Quiz
                    </button>
                  )}
                  
                  {showQuiz && quizItems.length > 0 && !quizResult && (
                    <div className="bg-gray-50 dark:bg-gray-900 p-4 rounded-lg">
                      <h4 className="font-semibold mb-3">Answer these questions:</h4>
                      {quizItems.map((item: any) => (
                        <div key={item.idx} className="mb-4">
                          <p className="font-medium mb-2">
                            {item.idx + 1}. {item.question}
                          </p>
                          <div className="space-y-2">
                            {item.choices.map((choice: string, choiceIdx: number) => (
                              <label key={choiceIdx} className="flex items-center">
                                <input
                                  type="radio"
                                  name={`q${item.idx}`}
                                  value={choiceIdx}
                                  onChange={() => setQuizAnswers({
                                    ...quizAnswers,
                                    [item.idx]: choiceIdx
                                  })}
                                  className="mr-2"
                                />
                                <span>{choice}</span>
                              </label>
                            ))}
                          </div>
                        </div>
                      ))}
                      <button
                        onClick={gradeQuiz}
                        disabled={Object.keys(quizAnswers).length < quizItems.length}
                        className="bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed font-medium"
                      >
                        Submit Quiz
                      </button>
                    </div>
                  )}
                  
                  {quizResult && (
                    <div className="bg-green-50 dark:bg-green-900 p-4 rounded-lg">
                      <h4 className="font-semibold mb-2">Quiz Results</h4>
                      <p className="text-lg mb-2">
                        Score: {quizResult.score}/{quizResult.total} ({quizResult.percentage}%)
                      </p>
                      {quizResult.inferred_mastered?.length > 0 && (
                        <div>
                          <p className="font-medium mb-1">Skills added to baseline:</p>
                          <div className="flex flex-wrap gap-2">
                            {quizResult.inferred_mastered.map((skill: string) => (
                              <span key={skill} className="bg-green-200 dark:bg-green-700 px-2 py-1 rounded text-sm">
                                {skill}
                              </span>
                            ))}
                          </div>
                        </div>
                      )}
                      <button
                        onClick={() => {
                          setShowQuiz(false)
                          setQuizResult(null)
                          setQuizItems([])
                        }}
                        className="mt-3 text-blue-600 hover:underline"
                      >
                        Close Quiz
                      </button>
                    </div>
                  )}
                </div>
"""
    
    # Insert quiz UI before the generate button
    page_tsx = page_tsx.replace(
        '                <div className="md:col-span-2">',
        quiz_ui + '\n                <div className="md:col-span-2">'
    )

# Update major options to include new majors
if '"public_health"' not in page_tsx:
    major_options = '''                    <option value="cs">Computer Science</option>
                    <option value="ee">Electrical Engineering</option>
                    <option value="physics">Physics</option>
                    <option value="data-science">Data Science</option>
                    <option value="public_health">Public Health</option>
                    <option value="materials">Materials Science</option>'''
    
    page_tsx = re.sub(
        r'<option value="cs">.*?</option>\s*<option value="ee">.*?</option>\s*<option value="physics">.*?</option>\s*<option value="data-science">.*?</option>',
        major_options,
        page_tsx,
        flags=re.DOTALL
    )

# Save updated page.tsx
with open(page_path, "w") as f:
    f.write(page_tsx)

print("\n✅ AI Path Advisor Extended Successfully!")
print("\n📊 Added:")
print("  - Public Health major with 10 skills, 3 modules, 9 resources")
print("  - Materials Science major with 10 skills, 3 modules, 10 resources")
print("  - Quiz system with 5 questions per major")
print("  - Frontend quiz UI with skill assessment")
print("\n🚀 To test:")
print("  1. Backend:  cd backend && uvicorn main:app --reload")
print("  2. Frontend: cd frontend && npm run dev")
print("  3. Try the quiz for any major to assess baseline skills")
print("\n📝 Quiz API:")
print("  POST /quiz/start - Start a quiz")
print("  POST /quiz/grade - Grade and get mastered skills")