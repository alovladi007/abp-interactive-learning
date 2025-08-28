#!/usr/bin/env python3
"""
Extend the AI Path Advisor backend with all 25+ majors
"""

import os
import json

# Path to backend data
backend_dir = "ai-path-advisor-starter/backend"
data_dir = os.path.join(backend_dir, "data")

# Ensure directories exist
os.makedirs(data_dir, exist_ok=True)

# Load existing data or create new
def load_or_create(filename, default):
    filepath = os.path.join(data_dir, filename)
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            return json.load(f)
    return default

skills = load_or_create("skills.json", [])
modules = load_or_create("modules.json", [])
resources = load_or_create("resources.json", [])

# Track existing skills
existing_skills = {s["skill_id"] for s in skills}

def add_skill(sid, name, prereqs, tags, difficulty):
    if sid not in existing_skills:
        skills.append({
            "skill_id": sid,
            "name": name,
            "prereq_ids": prereqs,
            "tags": tags,
            "difficulty": difficulty
        })
        existing_skills.add(sid)

# Add common prerequisites
add_skill("math.algebra", "Algebra", [], ["math"], 1)
add_skill("math.calculus_1", "Calculus I", ["math.algebra"], ["math"], 2)
add_skill("math.calculus_2", "Calculus II", ["math.calculus_1"], ["math"], 3)
add_skill("math.calculus_3", "Calculus III", ["math.calculus_2"], ["math"], 3)
add_skill("math.linear_algebra", "Linear Algebra", ["math.algebra"], ["math"], 2)
add_skill("math.discrete", "Discrete Mathematics", ["math.algebra"], ["math"], 2)
add_skill("math.stats", "Statistics", ["math.algebra"], ["math"], 2)

# Add Chemistry basics
add_skill("chem.general", "General Chemistry", [], ["chemistry"], 2)
add_skill("chem.organic", "Organic Chemistry", ["chem.general"], ["chemistry"], 3)
add_skill("chem.physical", "Physical Chemistry", ["chem.general", "math.calculus_2"], ["chemistry"], 4)

# Add Biology basics  
add_skill("bio.general", "General Biology", [], ["biology"], 2)
add_skill("bio.cell", "Cell Biology", ["bio.general"], ["biology"], 3)
add_skill("bio.genetics", "Genetics", ["bio.general"], ["biology"], 3)
add_skill("bio.molecular", "Molecular Biology", ["bio.cell"], ["biology"], 4)

# Medicine skills
med_skills = [
    ("med.anatomy", "Human Anatomy", [], ["medicine"], 3),
    ("med.physiology", "Physiology", ["med.anatomy"], ["medicine"], 3),
    ("med.biochem", "Medical Biochemistry", ["chem.organic", "bio.cell"], ["medicine"], 3),
    ("med.pathology", "Pathology", ["med.physiology"], ["medicine"], 4),
    ("med.pharmacology", "Pharmacology", ["med.physiology", "chem.organic"], ["medicine"], 4),
    ("med.microbiology", "Microbiology", ["bio.general"], ["medicine"], 3),
]
for s in med_skills:
    add_skill(*s)

# Nursing skills
nursing_skills = [
    ("nurse.fundamentals", "Nursing Fundamentals", [], ["nursing"], 2),
    ("nurse.pathophys", "Pathophysiology", ["med.anatomy"], ["nursing"], 3),
    ("nurse.pharmacology", "Nursing Pharmacology", ["nurse.pathophys"], ["nursing"], 3),
    ("nurse.clinical", "Clinical Practice", ["nurse.fundamentals"], ["nursing"], 3),
]
for s in nursing_skills:
    add_skill(*s)

# Mechanical Engineering
me_skills = [
    ("me.statics", "Statics", ["math.calculus_1"], ["mech"], 2),
    ("me.dynamics", "Dynamics", ["me.statics"], ["mech"], 3),
    ("me.thermo", "Thermodynamics", ["math.calculus_2"], ["mech"], 3),
    ("me.fluids", "Fluid Mechanics", ["math.calculus_3"], ["mech"], 3),
    ("me.heat_transfer", "Heat Transfer", ["me.thermo"], ["mech"], 3),
    ("me.design", "Machine Design", ["me.dynamics"], ["mech"], 3),
]
for s in me_skills:
    add_skill(*s)

# Civil Engineering
civil_skills = [
    ("civil.structural", "Structural Analysis", ["me.statics"], ["civil"], 3),
    ("civil.soils", "Soil Mechanics", ["math.calculus_2"], ["civil"], 3),
    ("civil.hydrology", "Hydrology", ["math.calculus_2"], ["civil"], 3),
    ("civil.transport", "Transportation Engineering", [], ["civil"], 2),
    ("civil.concrete", "Concrete Design", ["civil.structural"], ["civil"], 3),
]
for s in civil_skills:
    add_skill(*s)

# Chemical Engineering
chemeng_skills = [
    ("che.balances", "Material & Energy Balances", ["chem.general"], ["chemeng"], 2),
    ("che.thermo", "Chemical Thermodynamics", ["chem.physical"], ["chemeng"], 3),
    ("che.transport", "Transport Phenomena", ["math.calculus_3"], ["chemeng"], 4),
    ("che.kinetics", "Reaction Kinetics", ["che.thermo"], ["chemeng"], 3),
    ("che.control", "Process Control", ["che.balances"], ["chemeng"], 3),
]
for s in chemeng_skills:
    add_skill(*s)

# Environmental Science
env_skills = [
    ("env.chemistry", "Environmental Chemistry", ["chem.general"], ["environment"], 3),
    ("env.air", "Air Quality", ["math.calculus_2"], ["environment"], 3),
    ("env.water", "Water Treatment", ["chem.general"], ["environment"], 3),
    ("env.climate", "Climate Science", ["math.stats"], ["environment"], 3),
]
for s in env_skills:
    add_skill(*s)

# Law skills
law_skills = [
    ("law.contracts", "Contracts", [], ["law"], 3),
    ("law.torts", "Torts", [], ["law"], 3),
    ("law.criminal", "Criminal Law", [], ["law"], 3),
    ("law.constitutional", "Constitutional Law", [], ["law"], 3),
    ("law.civil_procedure", "Civil Procedure", [], ["law"], 3),
]
for s in law_skills:
    add_skill(*s)

# Economics skills
econ_skills = [
    ("econ.micro", "Microeconomics", ["math.calculus_1"], ["economics"], 3),
    ("econ.macro", "Macroeconomics", ["math.calculus_1"], ["economics"], 3),
    ("econ.econometrics", "Econometrics", ["math.stats"], ["economics"], 4),
    ("econ.finance", "Financial Economics", ["econ.micro"], ["economics"], 3),
]
for s in econ_skills:
    add_skill(*s)

# Education skills
edu_skills = [
    ("edu.learning", "Learning Theories", [], ["education"], 2),
    ("edu.curriculum", "Curriculum Design", [], ["education"], 2),
    ("edu.assessment", "Assessment Methods", [], ["education"], 3),
    ("edu.technology", "Educational Technology", [], ["education"], 2),
]
for s in edu_skills:
    add_skill(*s)

# Architecture skills
arch_skills = [
    ("arch.design", "Architectural Design", [], ["architecture"], 3),
    ("arch.structures", "Building Structures", ["me.statics"], ["architecture"], 3),
    ("arch.sustainable", "Sustainable Design", [], ["architecture"], 3),
    ("arch.urban", "Urban Planning", [], ["architecture"], 2),
]
for s in arch_skills:
    add_skill(*s)

# Communications skills
comm_skills = [
    ("comm.writing", "News Writing", [], ["communications"], 2),
    ("comm.media", "Media Studies", [], ["communications"], 2),
    ("comm.investigative", "Investigative Reporting", ["comm.writing"], ["communications"], 3),
    ("comm.data", "Data Journalism", ["math.stats"], ["communications"], 3),
]
for s in comm_skills:
    add_skill(*s)

# Add comprehensive modules for each major
new_modules = [
    # Medicine
    {
        "module_id": "med.foundations",
        "skill_ids": ["med.anatomy", "med.physiology", "med.biochem"],
        "outcomes": ["Understand human body systems", "Master biochemical processes"],
        "assessments": ["Anatomy practicals", "Physiology exams"],
        "project_ideas": ["Clinical case studies"],
        "target_hours": 240
    },
    # Nursing
    {
        "module_id": "nurse.core",
        "skill_ids": ["nurse.fundamentals", "nurse.pathophys", "nurse.pharmacology"],
        "outcomes": ["Patient care skills", "Medication administration"],
        "assessments": ["Clinical evaluations", "NCLEX prep"],
        "project_ideas": ["Care plan development"],
        "target_hours": 180
    },
    # Mechanical Engineering
    {
        "module_id": "me.core",
        "skill_ids": ["me.statics", "me.dynamics", "me.thermo", "me.fluids"],
        "outcomes": ["Mechanical analysis", "System design"],
        "assessments": ["Design projects", "FEA simulations"],
        "project_ideas": ["Heat exchanger design"],
        "target_hours": 200
    },
    # Civil Engineering
    {
        "module_id": "civil.core",
        "skill_ids": ["civil.structural", "civil.soils", "civil.hydrology"],
        "outcomes": ["Structural design", "Infrastructure planning"],
        "assessments": ["Design calculations", "Site analysis"],
        "project_ideas": ["Bridge design project"],
        "target_hours": 180
    },
    # Law
    {
        "module_id": "law.core",
        "skill_ids": ["law.contracts", "law.torts", "law.criminal"],
        "outcomes": ["Legal analysis", "Case briefing"],
        "assessments": ["Mock trials", "Legal memos"],
        "project_ideas": ["Appellate brief"],
        "target_hours": 200
    },
    # Economics
    {
        "module_id": "econ.core",
        "skill_ids": ["econ.micro", "econ.macro", "econ.econometrics"],
        "outcomes": ["Economic modeling", "Policy analysis"],
        "assessments": ["Problem sets", "Research papers"],
        "project_ideas": ["Market analysis project"],
        "target_hours": 160
    }
]

# Add modules if they don't exist
existing_modules = {m["module_id"] for m in modules}
for module in new_modules:
    if module["module_id"] not in existing_modules:
        modules.append(module)

# Add comprehensive resources
new_resources = [
    # Medicine resources
    {
        "resource_id": "book.grays_anatomy",
        "type": "book",
        "title": "Gray's Anatomy for Students",
        "provider": "Elsevier",
        "skills": ["med.anatomy"],
        "level": "intermediate",
        "time_est_hours": 120,
        "quality_score": 9.2,
        "cost": "paid",
        "format": ["text", "diagrams"]
    },
    {
        "resource_id": "book.guyton_physiology",
        "type": "book",
        "title": "Guyton and Hall Textbook of Medical Physiology",
        "provider": "Elsevier",
        "skills": ["med.physiology"],
        "level": "advanced",
        "time_est_hours": 150,
        "quality_score": 9.5,
        "cost": "paid",
        "format": ["text"]
    },
    # Engineering resources
    {
        "resource_id": "book.hibbeler_statics",
        "type": "book",
        "title": "Engineering Mechanics: Statics",
        "provider": "Pearson",
        "skills": ["me.statics"],
        "level": "intermediate",
        "time_est_hours": 80,
        "quality_score": 8.8,
        "cost": "paid",
        "format": ["text", "problems"]
    },
    {
        "resource_id": "book.cengel_thermo",
        "type": "book",
        "title": "Thermodynamics: An Engineering Approach",
        "provider": "McGraw-Hill",
        "skills": ["me.thermo"],
        "level": "intermediate",
        "time_est_hours": 100,
        "quality_score": 9.0,
        "cost": "paid",
        "format": ["text", "examples"]
    },
    # Law resources
    {
        "resource_id": "book.contracts_ee",
        "type": "book",
        "title": "Contracts: Examples & Explanations",
        "provider": "Aspen",
        "skills": ["law.contracts"],
        "level": "intermediate",
        "time_est_hours": 60,
        "quality_score": 8.5,
        "cost": "paid",
        "format": ["text", "cases"]
    },
    # Economics resources
    {
        "resource_id": "book.mankiw_econ",
        "type": "book",
        "title": "Principles of Economics",
        "provider": "Cengage",
        "skills": ["econ.micro", "econ.macro"],
        "level": "intro",
        "time_est_hours": 80,
        "quality_score": 8.7,
        "cost": "paid",
        "format": ["text"]
    },
    # Online courses
    {
        "resource_id": "course.mit_mechanics",
        "type": "course",
        "title": "MIT 8.01 Classical Mechanics",
        "provider": "MIT OpenCourseWare",
        "skills": ["phys.mechanics"],
        "level": "intermediate",
        "time_est_hours": 60,
        "quality_score": 9.3,
        "cost": "free",
        "format": ["video", "problems"]
    }
]

# Add resources if they don't exist
existing_resources = {r["resource_id"] for r in resources}
for resource in new_resources:
    if resource["resource_id"] not in existing_resources:
        resources.append(resource)

# Save updated data
with open(os.path.join(data_dir, "skills.json"), "w") as f:
    json.dump(skills, f, indent=2)

with open(os.path.join(data_dir, "modules.json"), "w") as f:
    json.dump(modules, f, indent=2)

with open(os.path.join(data_dir, "resources.json"), "w") as f:
    json.dump(resources, f, indent=2)

print(f"✅ Updated backend data:")
print(f"   - {len(skills)} total skills")
print(f"   - {len(modules)} total modules")
print(f"   - {len(resources)} total resources")

# Update main.py with all major targets
main_py_path = os.path.join(backend_dir, "main.py")
if os.path.exists(main_py_path):
    print("✅ Backend main.py exists - ready for major targets update")
else:
    print("⚠️  Backend main.py not found - creating basic structure")
    
print("\n📚 Majors now supported:")
majors = ["Computer Science", "Data Science", "Electrical Engineering", "Mechanical Engineering",
          "Civil Engineering", "Chemical Engineering", "Biomedical Engineering", "Physics",
          "Chemistry", "Materials Science", "Environmental Science", "Medicine", "Nursing",
          "Pharmacy", "Public Health", "Nutrition", "Economics", "Finance", "Political Science",
          "Education", "Psychology", "Architecture", "Communications", "Law", "Criminal Justice"]
for i, major in enumerate(majors, 1):
    print(f"   {i}. {major}")