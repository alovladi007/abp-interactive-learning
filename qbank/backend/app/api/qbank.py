"""
QBank API Endpoints
RESTful API for adaptive testing and question bank management
"""

from fastapi import APIRouter, HTTPException, Depends, Query, Body
from typing import List, Dict, Optional, Any
from datetime import datetime, timedelta
import uuid
import random
from pydantic import BaseModel, Field

# Pydantic models for request/response
class SessionStartRequest(BaseModel):
    user_id: str
    test_type: str = Field(..., description="Type of test (SAT, ACT, GRE, etc.)")
    subject: str = Field(..., description="Subject area")
    target_questions: int = Field(default=20, ge=5, le=100)
    time_limit_minutes: Optional[int] = Field(default=None, ge=10, le=300)

class SessionResponse(BaseModel):
    session_id: str
    session_token: str
    status: str
    test_type: str
    subject: str
    target_questions: int
    time_limit: Optional[int]
    created_at: datetime

class QuestionResponse(BaseModel):
    question_id: int
    content: str
    question_type: str
    options: Optional[List[str]]
    subject: str
    topic: str
    question_number: int
    total_questions: int
    time_remaining: Optional[int]

class SubmitAnswerRequest(BaseModel):
    session_token: str
    question_id: int
    answer: str
    response_time: float = Field(..., ge=0, description="Response time in seconds")

class AnswerFeedback(BaseModel):
    is_correct: bool
    correct_answer: str
    explanation: Optional[str]
    ability_estimate: float
    confidence_interval: tuple
    questions_remaining: int
    next_question_available: bool

class PerformanceAnalytics(BaseModel):
    session_id: str
    ability_estimate: float
    ability_se: float
    confidence_interval: tuple
    questions_answered: int
    correct_answers: int
    accuracy: float
    average_response_time: float
    ability_history: List[float]
    topic_performance: Dict[str, Dict]
    strengths: List[str]
    weaknesses: List[str]
    percentile_rank: float

class CalibrationStatus(BaseModel):
    last_run: Optional[datetime]
    next_scheduled: datetime
    items_needing_calibration: int
    average_response_count: float
    calibration_quality: str

class ItemAnalysis(BaseModel):
    item_id: int
    discrimination: float
    difficulty: float
    guessing: float
    exposure_rate: float
    total_responses: int
    p_value: float
    point_biserial: float
    infit: float
    outfit: float
    flags: List[str]

# Create router
router = APIRouter()

# In-memory storage for demo (would use database in production)
sessions = {}
questions_db = []

# Initialize sample questions
def init_sample_questions():
    """Initialize sample question database"""
    global questions_db
    if not questions_db:
        subjects = ["Mathematics", "Science", "English", "History"]
        topics = {
            "Mathematics": ["Algebra", "Geometry", "Calculus", "Statistics"],
            "Science": ["Physics", "Chemistry", "Biology", "Earth Science"],
            "English": ["Reading", "Writing", "Grammar", "Vocabulary"],
            "History": ["US History", "World History", "Ancient History", "Modern History"]
        }
        
        for i in range(1, 501):  # Create 500 sample questions
            subject = random.choice(subjects)
            topic = random.choice(topics[subject])
            
            questions_db.append({
                'id': i,
                'content': f"Sample question {i} for {topic}",
                'subject': subject,
                'topic': topic,
                'question_type': 'multiple_choice',
                'options': [f"Option {j}" for j in ['A', 'B', 'C', 'D']],
                'correct_answer': random.choice(['A', 'B', 'C', 'D']),
                'explanation': f"This is the explanation for question {i}",
                'discrimination': random.uniform(0.5, 2.0),
                'difficulty': random.uniform(-3, 3),
                'guessing': random.uniform(0.15, 0.35),
                'exposure_rate': 0.0,
                'selection_probability': 1.0
            })

init_sample_questions()

# Session Management Endpoints

@router.post("/sessions/start", response_model=SessionResponse)
async def start_session(request: SessionStartRequest):
    """Start a new adaptive testing session"""
    session_id = str(uuid.uuid4())
    session_token = str(uuid.uuid4())
    
    session = {
        'session_id': session_id,
        'session_token': session_token,
        'user_id': request.user_id,
        'test_type': request.test_type,
        'subject': request.subject,
        'target_questions': request.target_questions,
        'time_limit': request.time_limit_minutes,
        'status': 'active',
        'created_at': datetime.now(),
        'questions_answered': 0,
        'correct_answers': 0,
        'ability_estimate': 0.0,
        'ability_se': 1.0,
        'administered_items': [],
        'responses': [],
        'ability_history': [0.0]
    }
    
    sessions[session_token] = session
    
    return SessionResponse(
        session_id=session_id,
        session_token=session_token,
        status='active',
        test_type=request.test_type,
        subject=request.subject,
        target_questions=request.target_questions,
        time_limit=request.time_limit_minutes,
        created_at=session['created_at']
    )

@router.get("/sessions/{session_token}/status")
async def get_session_status(session_token: str):
    """Get current session status"""
    if session_token not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session = sessions[session_token]
    time_elapsed = (datetime.now() - session['created_at']).total_seconds()
    
    return {
        'status': session['status'],
        'questions_answered': session['questions_answered'],
        'target_questions': session['target_questions'],
        'ability_estimate': session['ability_estimate'],
        'ability_se': session['ability_se'],
        'time_elapsed': int(time_elapsed),
        'time_limit': session['time_limit']
    }

# Question Delivery Endpoints

@router.get("/questions/next", response_model=QuestionResponse)
async def get_next_question(session_token: str = Query(...)):
    """Get next adaptive question based on current ability estimate"""
    if session_token not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session = sessions[session_token]
    
    if session['status'] != 'active':
        raise HTTPException(status_code=400, detail="Session is not active")
    
    if session['questions_answered'] >= session['target_questions']:
        raise HTTPException(status_code=400, detail="Test completed")
    
    # Filter questions by subject
    subject_questions = [q for q in questions_db if q['subject'] == session['subject']]
    
    # Filter out already administered questions
    available = [q for q in subject_questions if q['id'] not in session['administered_items']]
    
    if not available:
        raise HTTPException(status_code=404, detail="No more questions available")
    
    # Select question based on maximum information (simplified)
    theta = session['ability_estimate']
    best_question = None
    max_info = -1
    
    for q in available[:50]:  # Check top 50 to limit computation
        # Calculate Fisher information (simplified)
        a = q['discrimination']
        b = q['difficulty']
        c = q['guessing']
        
        # 3PL probability
        p = c + (1 - c) / (1 + np.exp(-1.702 * a * (theta - b)))
        
        # Fisher information
        if c < p < 1:
            info = (1.702 ** 2) * (a ** 2) * ((p - c) ** 2) / ((1 - c) ** 2 * p * (1 - p))
        else:
            info = 0
        
        if info > max_info:
            max_info = info
            best_question = q
    
    if not best_question:
        best_question = random.choice(available)
    
    # Calculate time remaining
    time_remaining = None
    if session['time_limit']:
        time_elapsed = (datetime.now() - session['created_at']).total_seconds() / 60
        time_remaining = max(0, session['time_limit'] - int(time_elapsed))
    
    return QuestionResponse(
        question_id=best_question['id'],
        content=best_question['content'],
        question_type=best_question['question_type'],
        options=best_question['options'],
        subject=best_question['subject'],
        topic=best_question['topic'],
        question_number=session['questions_answered'] + 1,
        total_questions=session['target_questions'],
        time_remaining=time_remaining
    )

# Response Processing Endpoints

@router.post("/responses/submit", response_model=AnswerFeedback)
async def submit_answer(request: SubmitAnswerRequest):
    """Submit answer and get feedback"""
    if request.session_token not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session = sessions[request.session_token]
    
    # Find question
    question = next((q for q in questions_db if q['id'] == request.question_id), None)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    # Check answer
    is_correct = request.answer == question['correct_answer']
    
    # Update session
    session['questions_answered'] += 1
    if is_correct:
        session['correct_answers'] += 1
    
    session['administered_items'].append(request.question_id)
    
    # Store response
    response_data = {
        'question_id': request.question_id,
        'answer': request.answer,
        'is_correct': is_correct,
        'response_time': request.response_time,
        'ability_before': session['ability_estimate']
    }
    
    # Update ability estimate (simplified EAP)
    responses = session['responses'] + [response_data]
    
    # Simple ability update
    if is_correct:
        session['ability_estimate'] += 0.3 / (session['questions_answered'] ** 0.5)
    else:
        session['ability_estimate'] -= 0.3 / (session['questions_answered'] ** 0.5)
    
    session['ability_estimate'] = max(-3, min(3, session['ability_estimate']))
    session['ability_se'] = 1.0 / (session['questions_answered'] ** 0.5)
    
    response_data['ability_after'] = session['ability_estimate']
    session['responses'].append(response_data)
    session['ability_history'].append(session['ability_estimate'])
    
    # Check if test should end
    questions_remaining = session['target_questions'] - session['questions_answered']
    next_available = questions_remaining > 0 and session['status'] == 'active'
    
    if questions_remaining == 0:
        session['status'] = 'completed'
    
    # Calculate confidence interval
    z_score = 1.96  # 95% confidence
    ci_lower = session['ability_estimate'] - z_score * session['ability_se']
    ci_upper = session['ability_estimate'] + z_score * session['ability_se']
    
    return AnswerFeedback(
        is_correct=is_correct,
        correct_answer=question['correct_answer'],
        explanation=question['explanation'],
        ability_estimate=session['ability_estimate'],
        confidence_interval=(ci_lower, ci_upper),
        questions_remaining=questions_remaining,
        next_question_available=next_available
    )

# Analytics Endpoints

@router.get("/analytics/performance/{session_token}", response_model=PerformanceAnalytics)
async def get_performance_analytics(session_token: str):
    """Get detailed performance analytics for a session"""
    if session_token not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session = sessions[session_token]
    
    # Calculate topic performance
    topic_performance = {}
    for resp in session['responses']:
        q = next((q for q in questions_db if q['id'] == resp['question_id']), None)
        if q:
            topic = q['topic']
            if topic not in topic_performance:
                topic_performance[topic] = {'correct': 0, 'total': 0}
            topic_performance[topic]['total'] += 1
            if resp['is_correct']:
                topic_performance[topic]['correct'] += 1
    
    # Calculate percentages
    for topic in topic_performance:
        total = topic_performance[topic]['total']
        correct = topic_performance[topic]['correct']
        topic_performance[topic]['percentage'] = (correct / total * 100) if total > 0 else 0
    
    # Identify strengths and weaknesses
    strengths = [t for t, p in topic_performance.items() if p['percentage'] >= 70]
    weaknesses = [t for t, p in topic_performance.items() if p['percentage'] < 50]
    
    # Calculate percentile (simplified - would use norm tables in production)
    from scipy.stats import norm
    percentile = norm.cdf(session['ability_estimate']) * 100
    
    # Calculate average response time
    avg_response_time = np.mean([r['response_time'] for r in session['responses']]) if session['responses'] else 0
    
    # Confidence interval
    z_score = 1.96
    ci_lower = session['ability_estimate'] - z_score * session['ability_se']
    ci_upper = session['ability_estimate'] + z_score * session['ability_se']
    
    return PerformanceAnalytics(
        session_id=session['session_id'],
        ability_estimate=session['ability_estimate'],
        ability_se=session['ability_se'],
        confidence_interval=(ci_lower, ci_upper),
        questions_answered=session['questions_answered'],
        correct_answers=session['correct_answers'],
        accuracy=session['correct_answers'] / session['questions_answered'] if session['questions_answered'] > 0 else 0,
        average_response_time=avg_response_time,
        ability_history=session['ability_history'],
        topic_performance=topic_performance,
        strengths=strengths,
        weaknesses=weaknesses,
        percentile_rank=percentile
    )

# Calibration Endpoints

@router.get("/calibration/status", response_model=CalibrationStatus)
async def get_calibration_status():
    """Get current calibration status"""
    # Simulated calibration status
    return CalibrationStatus(
        last_run=datetime.now() - timedelta(hours=12),
        next_scheduled=datetime.now() + timedelta(hours=12),
        items_needing_calibration=45,
        average_response_count=156.3,
        calibration_quality="good"
    )

@router.post("/calibration/run")
async def trigger_calibration(
    method: str = Query("MMLE", description="Calibration method"),
    min_responses: int = Query(30, description="Minimum responses required")
):
    """Trigger manual calibration run"""
    # In production, this would start an async calibration job
    calibration_id = str(uuid.uuid4())
    
    return {
        'calibration_id': calibration_id,
        'status': 'started',
        'method': method,
        'min_responses': min_responses,
        'estimated_duration': '5-10 minutes',
        'message': 'Calibration job started successfully'
    }

# Admin Endpoints

@router.get("/admin/items/analysis", response_model=List[ItemAnalysis])
async def get_item_analysis(
    subject: Optional[str] = Query(None),
    min_responses: int = Query(0),
    limit: int = Query(10, le=100)
):
    """Get item analysis report"""
    # Filter questions
    filtered = questions_db
    if subject:
        filtered = [q for q in filtered if q['subject'] == subject]
    
    # Create analysis for each item (simplified)
    analyses = []
    for q in filtered[:limit]:
        # Simulated statistics
        total_responses = random.randint(50, 500)
        correct_responses = int(total_responses * random.uniform(0.3, 0.8))
        
        analysis = ItemAnalysis(
            item_id=q['id'],
            discrimination=q['discrimination'],
            difficulty=q['difficulty'],
            guessing=q['guessing'],
            exposure_rate=random.uniform(0.1, 0.3),
            total_responses=total_responses,
            p_value=correct_responses / total_responses,
            point_biserial=random.uniform(0.2, 0.6),
            infit=random.uniform(0.8, 1.2),
            outfit=random.uniform(0.8, 1.2),
            flags=[]
        )
        
        # Add flags for problematic items
        if analysis.discrimination < 0.5:
            analysis.flags.append("low_discrimination")
        if analysis.infit < 0.7 or analysis.infit > 1.3:
            analysis.flags.append("poor_fit")
        if analysis.exposure_rate > 0.25:
            analysis.flags.append("overexposed")
        
        analyses.append(analysis)
    
    return analyses

@router.get("/admin/exposure/report")
async def get_exposure_report():
    """Get exposure rate analysis"""
    # Calculate exposure statistics
    exposure_stats = {
        'mean_exposure': 0.18,
        'median_exposure': 0.17,
        'max_exposure': 0.25,
        'min_exposure': 0.02,
        'overexposed_items': 3,
        'underutilized_items': 12,
        'exposure_distribution': {
            '0-10%': 45,
            '10-15%': 120,
            '15-20%': 180,
            '20-25%': 150,
            '>25%': 5
        },
        'sympson_hetter_effectiveness': 0.92,
        'recommendations': [
            "3 items exceeding maximum exposure rate",
            "Consider rotating overexposed items",
            "12 high-quality items are underutilized"
        ]
    }
    
    return exposure_stats

# Import numpy for calculations
import numpy as np