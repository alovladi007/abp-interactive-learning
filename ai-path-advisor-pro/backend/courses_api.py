"""
Course Management API - Provides detailed course information with full syllabi
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import json
import os

router = APIRouter(prefix="/courses", tags=["courses"])

# Load course data
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

def load_courses():
    """Load all course data from JSON files"""
    courses = {}
    
    # Load main courses file
    main_courses_path = os.path.join(DATA_DIR, "courses.json")
    if os.path.exists(main_courses_path):
        with open(main_courses_path, 'r') as f:
            courses.update(json.load(f))
    
    # Load additional course files
    for filename in os.listdir(DATA_DIR):
        if filename.startswith("courses_") and filename.endswith(".json"):
            with open(os.path.join(DATA_DIR, filename), 'r') as f:
                courses.update(json.load(f))
    
    return courses

COURSES = load_courses()

# Pydantic models
class CourseTopic(BaseModel):
    week: int
    topic: str
    content: str

class CourseAssessment(BaseModel):
    type: str
    weight: str
    description: str

class CourseSyllabus(BaseModel):
    objectives: List[str]
    topics: List[CourseTopic]
    assessments: List[CourseAssessment]
    textbooks: List[str]

class Course(BaseModel):
    id: str
    name: str
    credits: int
    prerequisites: List[str]
    description: str
    syllabus: CourseSyllabus

class CourseListItem(BaseModel):
    id: str
    name: str
    credits: int
    prerequisites: List[str]
    description: str

# API Endpoints
@router.get("/majors")
def list_course_majors():
    """List all majors with course data"""
    return list(COURSES.keys())

@router.get("/major/{major}")
def get_major_courses(major: str) -> List[CourseListItem]:
    """Get all courses for a major"""
    if major not in COURSES:
        raise HTTPException(status_code=404, detail=f"Major {major} not found")
    
    return [
        CourseListItem(
            id=course["id"],
            name=course["name"],
            credits=course["credits"],
            prerequisites=course["prerequisites"],
            description=course["description"]
        )
        for course in COURSES[major]
    ]

@router.get("/major/{major}/top")
def get_top_courses(major: str, limit: int = 12) -> List[Course]:
    """Get top N most important courses for a major"""
    if major not in COURSES:
        raise HTTPException(status_code=404, detail=f"Major {major} not found")
    
    # Return first N courses (already ordered by importance in JSON)
    courses = COURSES[major][:limit]
    return [Course(**course) for course in courses]

@router.get("/major/{major}/course/{course_id}")
def get_course_details(major: str, course_id: str) -> Course:
    """Get detailed information about a specific course"""
    if major not in COURSES:
        raise HTTPException(status_code=404, detail=f"Major {major} not found")
    
    for course in COURSES[major]:
        if course["id"] == course_id:
            return Course(**course)
    
    raise HTTPException(status_code=404, detail=f"Course {course_id} not found in major {major}")

@router.get("/major/{major}/prerequisites")
def get_prerequisite_graph(major: str):
    """Get prerequisite relationships for all courses in a major"""
    if major not in COURSES:
        raise HTTPException(status_code=404, detail=f"Major {major} not found")
    
    graph = {}
    for course in COURSES[major]:
        graph[course["id"]] = {
            "name": course["name"],
            "prerequisites": course["prerequisites"]
        }
    
    return graph

@router.get("/major/{major}/syllabus/{course_id}/week/{week}")
def get_weekly_content(major: str, course_id: str, week: int):
    """Get specific week's content from a course syllabus"""
    if major not in COURSES:
        raise HTTPException(status_code=404, detail=f"Major {major} not found")
    
    for course in COURSES[major]:
        if course["id"] == course_id:
            topics = course["syllabus"]["topics"]
            for topic in topics:
                if topic["week"] == week:
                    return topic
            raise HTTPException(status_code=404, detail=f"Week {week} not found")
    
    raise HTTPException(status_code=404, detail=f"Course {course_id} not found")

@router.get("/search")
def search_courses(query: str, major: Optional[str] = None):
    """Search courses by name or description"""
    results = []
    
    majors_to_search = [major] if major and major in COURSES else COURSES.keys()
    
    for maj in majors_to_search:
        for course in COURSES[maj]:
            if (query.lower() in course["name"].lower() or 
                query.lower() in course["description"].lower()):
                results.append({
                    "major": maj,
                    "course": CourseListItem(
                        id=course["id"],
                        name=course["name"],
                        credits=course["credits"],
                        prerequisites=course["prerequisites"],
                        description=course["description"]
                    )
                })
    
    return results

@router.get("/major/{major}/roadmap")
def generate_course_roadmap(major: str):
    """Generate a suggested course sequence for a major"""
    if major not in COURSES:
        raise HTTPException(status_code=404, detail=f"Major {major} not found")
    
    courses = COURSES[major]
    
    # Build dependency graph
    completed = set()
    roadmap = []
    semester = 1
    
    while len(completed) < len(courses):
        semester_courses = []
        
        for course in courses:
            if course["id"] not in completed:
                # Check if prerequisites are met
                if all(prereq in completed or prereq == "" 
                       for prereq in course["prerequisites"]):
                    semester_courses.append(course["id"])
                    if len(semester_courses) >= 4:  # Max 4 courses per semester
                        break
        
        if not semester_courses:
            # Add courses with external prerequisites
            for course in courses:
                if course["id"] not in completed:
                    semester_courses.append(course["id"])
                    if len(semester_courses) >= 4:
                        break
        
        if semester_courses:
            roadmap.append({
                "semester": semester,
                "courses": semester_courses,
                "total_credits": sum(
                    c["credits"] for c in courses 
                    if c["id"] in semester_courses
                )
            })
            completed.update(semester_courses)
            semester += 1
        else:
            break
    
    return {
        "major": major,
        "total_semesters": len(roadmap),
        "total_courses": len(completed),
        "roadmap": roadmap
    }

@router.get("/major/{major}/statistics")
def get_major_statistics(major: str):
    """Get statistics about courses in a major"""
    if major not in COURSES:
        raise HTTPException(status_code=404, detail=f"Major {major} not found")
    
    courses = COURSES[major]
    
    total_credits = sum(c["credits"] for c in courses)
    avg_credits = total_credits / len(courses) if courses else 0
    
    # Count prerequisites
    prereq_counts = {}
    for course in courses:
        prereq_count = len(course["prerequisites"])
        prereq_counts[prereq_count] = prereq_counts.get(prereq_count, 0) + 1
    
    # Assessment types
    assessment_types = {}
    for course in courses:
        for assessment in course["syllabus"]["assessments"]:
            assessment_type = assessment["type"]
            assessment_types[assessment_type] = assessment_types.get(assessment_type, 0) + 1
    
    return {
        "major": major,
        "total_courses": len(courses),
        "total_credits": total_credits,
        "average_credits": round(avg_credits, 2),
        "prerequisite_distribution": prereq_counts,
        "assessment_types": assessment_types,
        "total_topics": sum(len(c["syllabus"]["topics"]) for c in courses),
        "total_textbooks": sum(len(c["syllabus"]["textbooks"]) for c in courses)
    }