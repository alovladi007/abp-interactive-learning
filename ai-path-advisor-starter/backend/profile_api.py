"""
Academic Profile API - Manages user academic profiles and learning paths
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
import json
import os
from pathlib import Path

app = FastAPI(title="Academic Profile API", version="1.0.0")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data storage path
DATA_DIR = Path("./data/profiles")
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Models
class Course(BaseModel):
    id: str
    code: str
    name: str
    credits: int
    semester: str
    status: str = "enrolled"  # enrolled, completed, planned
    grade: Optional[str] = None

class AcademicProfile(BaseModel):
    user_id: str
    education_level: str = "undergraduate"
    current_level: str = "Undergraduate"
    active_courses: int = 0
    primary_field: Optional[str] = None
    primary_major: Optional[str] = None
    career_path: Optional[str] = None
    gpa: Optional[float] = None
    fields: List[str] = []
    courses: List[Course] = []
    study_hours: int = 15
    budget: str = "0"
    learning_style: str = "mixed"
    experience_level: str = "beginner"
    last_updated: str = datetime.now().isoformat()
    
class PathAdvisorData(BaseModel):
    field: str
    major: str
    career: str
    hours: str
    budget: str
    style: str
    level: str
    field_name: Optional[str] = None

class SuggestedCourse(BaseModel):
    code: str
    name: str
    credits: int
    reason: str
    priority: int = 1  # 1 = high, 2 = medium, 3 = low

# Career path to course mappings
CAREER_COURSE_MAPPINGS = {
    "ml-engineer": [
        {"code": "CS 4780", "name": "Machine Learning", "credits": 3, "reason": "Core ML concepts", "priority": 1},
        {"code": "CS 5785", "name": "Deep Learning", "credits": 3, "reason": "Neural networks and deep learning", "priority": 1},
        {"code": "MATH 4710", "name": "Probability Theory", "credits": 4, "reason": "Mathematical foundations", "priority": 2},
        {"code": "CS 4786", "name": "Machine Learning for Data Science", "credits": 3, "reason": "Applied ML", "priority": 2},
        {"code": "CS 5787", "name": "Statistical Inference", "credits": 3, "reason": "Statistical foundations", "priority": 3}
    ],
    "full-stack": [
        {"code": "CS 3110", "name": "Web Development", "credits": 3, "reason": "Frontend and backend basics", "priority": 1},
        {"code": "CS 4320", "name": "Database Systems", "credits": 3, "reason": "Data management", "priority": 1},
        {"code": "CS 5150", "name": "Software Engineering", "credits": 4, "reason": "Best practices", "priority": 2},
        {"code": "CS 4410", "name": "Operating Systems", "credits": 3, "reason": "System understanding", "priority": 3},
        {"code": "CS 5412", "name": "Cloud Computing", "credits": 3, "reason": "Modern deployment", "priority": 2}
    ],
    "data-engineer": [
        {"code": "CS 4320", "name": "Database Systems", "credits": 3, "reason": "Core data management", "priority": 1},
        {"code": "CS 5777", "name": "Big Data Technologies", "credits": 3, "reason": "Distributed systems", "priority": 1},
        {"code": "CS 4786", "name": "Data Mining", "credits": 3, "reason": "Data processing techniques", "priority": 2},
        {"code": "CS 5785", "name": "Applied Machine Learning", "credits": 3, "reason": "ML for data", "priority": 3},
        {"code": "CS 4744", "name": "Computational Linguistics", "credits": 3, "reason": "Text processing", "priority": 3}
    ],
    "embedded": [
        {"code": "ECE 3140", "name": "Embedded Systems", "credits": 4, "reason": "Core embedded programming", "priority": 1},
        {"code": "ECE 4760", "name": "Digital Systems Design", "credits": 4, "reason": "Hardware design", "priority": 1},
        {"code": "CS 4410", "name": "Operating Systems", "credits": 3, "reason": "RTOS concepts", "priority": 2},
        {"code": "ECE 5725", "name": "Embedded Operating Systems", "credits": 4, "reason": "Advanced embedded OS", "priority": 2},
        {"code": "ECE 4750", "name": "Computer Architecture", "credits": 3, "reason": "Hardware understanding", "priority": 3}
    ],
    "pre-med": [
        {"code": "BIOG 1440", "name": "Physiology", "credits": 4, "reason": "Medical school requirement", "priority": 1},
        {"code": "BIOMG 3300", "name": "Biochemistry", "credits": 4, "reason": "Medical school requirement", "priority": 1},
        {"code": "BIOG 1445", "name": "Anatomy", "credits": 4, "reason": "Medical school requirement", "priority": 1},
        {"code": "CHEM 3570", "name": "Organic Chemistry I", "credits": 4, "reason": "Medical school requirement", "priority": 1},
        {"code": "PHYS 2207", "name": "Physics I", "credits": 4, "reason": "Medical school requirement", "priority": 2}
    ]
}

# Helper functions
def get_profile_path(user_id: str) -> Path:
    return DATA_DIR / f"{user_id}.json"

def load_profile(user_id: str) -> Optional[AcademicProfile]:
    profile_path = get_profile_path(user_id)
    if profile_path.exists():
        with open(profile_path, 'r') as f:
            data = json.load(f)
            return AcademicProfile(**data)
    return None

def save_profile(profile: AcademicProfile):
    profile_path = get_profile_path(profile.user_id)
    with open(profile_path, 'w') as f:
        json.dump(profile.dict(), f, indent=2)

# API Endpoints
@app.get("/")
def root():
    return {
        "name": "Academic Profile API",
        "version": "1.0.0",
        "endpoints": [
            "/profile/{user_id}",
            "/profile/{user_id}/update",
            "/profile/{user_id}/courses",
            "/profile/{user_id}/suggested-courses",
            "/sync-path-advisor"
        ]
    }

@app.get("/profile/{user_id}", response_model=AcademicProfile)
def get_profile(user_id: str):
    """Get user's academic profile"""
    profile = load_profile(user_id)
    if not profile:
        # Create default profile
        profile = AcademicProfile(user_id=user_id)
        save_profile(profile)
    return profile

@app.post("/profile/{user_id}/update", response_model=AcademicProfile)
def update_profile(user_id: str, updates: Dict[str, Any]):
    """Update user's academic profile"""
    profile = load_profile(user_id)
    if not profile:
        profile = AcademicProfile(user_id=user_id)
    
    # Update fields
    for key, value in updates.items():
        if hasattr(profile, key):
            setattr(profile, key, value)
    
    profile.last_updated = datetime.now().isoformat()
    save_profile(profile)
    return profile

@app.post("/profile/{user_id}/sync-path-advisor", response_model=AcademicProfile)
def sync_path_advisor(user_id: str, data: PathAdvisorData):
    """Sync data from AI Path Advisor to academic profile"""
    profile = load_profile(user_id)
    if not profile:
        profile = AcademicProfile(user_id=user_id)
    
    # Update profile with path advisor data
    profile.primary_field = data.field
    profile.primary_major = data.major
    profile.career_path = data.career
    profile.study_hours = int(data.hours)
    profile.budget = data.budget
    profile.learning_style = data.style
    profile.experience_level = data.level
    
    # Add field if not present
    if data.field_name and data.field_name not in profile.fields:
        profile.fields.append(data.field_name)
    
    # Calculate active courses based on study hours
    profile.active_courses = min(5, max(1, int(data.hours) // 5))
    
    profile.last_updated = datetime.now().isoformat()
    save_profile(profile)
    return profile

@app.get("/profile/{user_id}/courses", response_model=List[Course])
def get_courses(user_id: str):
    """Get user's courses"""
    profile = load_profile(user_id)
    if not profile:
        return []
    return profile.courses

@app.post("/profile/{user_id}/courses/add", response_model=Course)
def add_course(user_id: str, course: Course):
    """Add a course to user's profile"""
    profile = load_profile(user_id)
    if not profile:
        profile = AcademicProfile(user_id=user_id)
    
    # Check if course already exists
    existing = next((c for c in profile.courses if c.code == course.code), None)
    if existing:
        raise HTTPException(status_code=400, detail="Course already exists")
    
    profile.courses.append(course)
    profile.active_courses = len([c for c in profile.courses if c.status == "enrolled"])
    profile.last_updated = datetime.now().isoformat()
    save_profile(profile)
    return course

@app.delete("/profile/{user_id}/courses/{course_code}")
def remove_course(user_id: str, course_code: str):
    """Remove a course from user's profile"""
    profile = load_profile(user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    profile.courses = [c for c in profile.courses if c.code != course_code]
    profile.active_courses = len([c for c in profile.courses if c.status == "enrolled"])
    profile.last_updated = datetime.now().isoformat()
    save_profile(profile)
    return {"message": "Course removed successfully"}

@app.get("/profile/{user_id}/suggested-courses", response_model=List[SuggestedCourse])
def get_suggested_courses(user_id: str):
    """Get suggested courses based on user's career path"""
    profile = load_profile(user_id)
    if not profile or not profile.career_path:
        return []
    
    # Get suggestions for career path
    suggestions = CAREER_COURSE_MAPPINGS.get(profile.career_path, [])
    
    # Filter out courses already in profile
    existing_codes = {c.code for c in profile.courses}
    filtered = [s for s in suggestions if s["code"] not in existing_codes]
    
    # Convert to SuggestedCourse objects
    return [SuggestedCourse(**s) for s in filtered]

@app.post("/profile/{user_id}/calculate-gpa")
def calculate_gpa(user_id: str):
    """Calculate GPA from completed courses"""
    profile = load_profile(user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    grade_points = {
        "A+": 4.3, "A": 4.0, "A-": 3.7,
        "B+": 3.3, "B": 3.0, "B-": 2.7,
        "C+": 2.3, "C": 2.0, "C-": 1.7,
        "D+": 1.3, "D": 1.0, "F": 0.0
    }
    
    completed_courses = [c for c in profile.courses if c.status == "completed" and c.grade]
    if not completed_courses:
        return {"gpa": None, "message": "No completed courses with grades"}
    
    total_points = 0
    total_credits = 0
    
    for course in completed_courses:
        if course.grade in grade_points:
            total_points += grade_points[course.grade] * course.credits
            total_credits += course.credits
    
    if total_credits == 0:
        return {"gpa": None, "message": "No valid grades found"}
    
    gpa = round(total_points / total_credits, 2)
    profile.gpa = gpa
    save_profile(profile)
    
    return {"gpa": gpa, "total_credits": total_credits}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)