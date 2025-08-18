# QBank v10 - Quiz API Endpoints
from fastapi import APIRouter, Depends, HTTPException, Query, Body
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import uuid
import random
import numpy as np

from app.core.database import get_db
from app.core.cache import cache
from app.models.orm import (
    QuizSession, QuizItem, UserResponse, Question, QuestionVersion,
    QuestionOption, ItemCalibration, UserAbility, Topic
)
from app.services.adaptive import AdaptiveSelector, IRTEngine
from app.services.calibration import CalibrationEngine

router = APIRouter(prefix="/v1/quizzes", tags=["quizzes"])

# Initialize engines
irt_engine = IRTEngine(model="3PL")
adaptive_selector = AdaptiveSelector(irt_engine)
calibration_engine = CalibrationEngine()

@router.post("/", response_model=Dict[str, Any])
async def create_quiz(
    user_id: str = Body(...),
    mode: str = Body("practice"),
    adaptive: bool = Body(True),
    exam_code: Optional[str] = Body(None),
    num_questions: int = Body(30),
    topics: Optional[List[str]] = Body(None),
    difficulty: Optional[List[str]] = Body(None),
    time_limit: int = Body(3600),
    db: AsyncSession = Depends(get_db)
):
    """Create a new quiz session"""
    
    # Create quiz session
    quiz_id = uuid.uuid4()
    expires_at = datetime.utcnow() + timedelta(seconds=time_limit)
    
    session = QuizSession(
        id=quiz_id,
        user_id=user_id,
        tenant_id=uuid.UUID("00000000-0000-0000-0000-000000000001"),
        mode=mode,
        adaptive=adaptive,
        exam_code=exam_code,
        config={
            "num_questions": num_questions,
            "topics": topics,
            "difficulty": difficulty,
            "time_limit": time_limit
        },
        started_at=datetime.utcnow(),
        expires_at=expires_at
    )
    
    db.add(session)
    
    # Get initial questions
    if adaptive:
        # Get user's current ability
        ability_query = select(UserAbility).where(
            UserAbility.user_id == user_id,
            UserAbility.topic_id == None  # Global ability
        )
        result = await db.execute(ability_query)
        user_ability = result.scalar_one_or_none()
        
        theta = user_ability.theta if user_ability else 0.0
        
        # Select first question adaptively
        first_question = await select_adaptive_question(
            db, theta, topics, difficulty, exam_code, []
        )
        
        if first_question:
            quiz_item = QuizItem(
                quiz_id=quiz_id,
                question_id=first_question["id"],
                version=first_question["version"],
                position=1,
                served_at=datetime.utcnow()
            )
            db.add(quiz_item)
    else:
        # Select random questions
        questions = await select_random_questions(
            db, num_questions, topics, difficulty, exam_code
        )
        
        for i, q in enumerate(questions[:num_questions], 1):
            quiz_item = QuizItem(
                quiz_id=quiz_id,
                question_id=q["id"],
                version=q["version"],
                position=i,
                served_at=datetime.utcnow()
            )
            db.add(quiz_item)
    
    await db.commit()
    
    # Cache session
    await cache.set_session(str(quiz_id), {
        "user_id": user_id,
        "mode": mode,
        "adaptive": adaptive,
        "theta": 0.0,
        "se": 1.0,
        "responses": []
    })
    
    return {
        "quiz_id": str(quiz_id),
        "mode": mode,
        "adaptive": adaptive,
        "num_questions": num_questions,
        "time_limit": time_limit,
        "expires_at": expires_at.isoformat()
    }

@router.get("/{quiz_id}/next", response_model=Dict[str, Any])
async def get_next_question(
    quiz_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Get the next question in the quiz"""
    
    # Get quiz session
    query = select(QuizSession).where(QuizSession.id == uuid.UUID(quiz_id))
    result = await db.execute(query)
    session = result.scalar_one_or_none()
    
    if not session:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    if session.completed_at:
        raise HTTPException(status_code=400, detail="Quiz already completed")
    
    if datetime.utcnow() > session.expires_at:
        raise HTTPException(status_code=400, detail="Quiz expired")
    
    # Get answered questions
    answered_query = select(UserResponse.question_id).where(
        UserResponse.quiz_id == uuid.UUID(quiz_id)
    )
    answered_result = await db.execute(answered_query)
    answered_ids = [r[0] for r in answered_result.fetchall()]
    
    # Get next question
    if session.adaptive:
        # Get current theta from cache
        cached_session = await cache.get_session(quiz_id)
        theta = cached_session.get("theta", 0.0) if cached_session else 0.0
        
        # Select next adaptive question
        next_q = await select_adaptive_question(
            db, theta, 
            session.config.get("topics"),
            session.config.get("difficulty"),
            session.exam_code,
            answered_ids
        )
        
        if next_q:
            # Add to quiz items
            position = len(answered_ids) + 1
            quiz_item = QuizItem(
                quiz_id=uuid.UUID(quiz_id),
                question_id=next_q["id"],
                version=next_q["version"],
                position=position,
                served_at=datetime.utcnow()
            )
            db.add(quiz_item)
            await db.commit()
    else:
        # Get pre-selected question
        items_query = select(QuizItem).where(
            QuizItem.quiz_id == uuid.UUID(quiz_id),
            ~QuizItem.question_id.in_(answered_ids) if answered_ids else True
        ).order_by(QuizItem.position)
        items_result = await db.execute(items_query)
        next_item = items_result.scalars().first()
        
        if next_item:
            # Get question details
            q_query = select(QuestionVersion, Question).join(
                Question, Question.id == QuestionVersion.question_id
            ).where(
                QuestionVersion.question_id == next_item.question_id,
                QuestionVersion.version == next_item.version
            )
            q_result = await db.execute(q_query)
            q_data = q_result.first()
            
            if q_data:
                qv, q = q_data
                
                # Get options
                opt_query = select(QuestionOption).where(
                    QuestionOption.question_version_id == qv.id
                )
                opt_result = await db.execute(opt_query)
                options = opt_result.scalars().all()
                
                next_q = {
                    "id": q.id,
                    "version": qv.version,
                    "stem": qv.stem_md,
                    "lead_in": qv.lead_in,
                    "options": [
                        {
                            "label": opt.option_label,
                            "text": opt.option_text_md
                        }
                        for opt in options
                    ],
                    "position": next_item.position,
                    "total": session.config.get("num_questions", 30)
                }
            else:
                next_q = None
        else:
            next_q = None
    
    if not next_q:
        # No more questions, complete the quiz
        session.completed_at = datetime.utcnow()
        
        # Calculate score
        score_query = select(
            func.count(UserResponse.id),
            func.sum(func.cast(UserResponse.is_correct, int))
        ).where(UserResponse.quiz_id == uuid.UUID(quiz_id))
        score_result = await db.execute(score_query)
        total, correct = score_result.first()
        
        session.score = (correct / total * 100) if total > 0 else 0
        await db.commit()
        
        return {
            "completed": True,
            "score": session.score,
            "total_questions": total,
            "correct_answers": correct
        }
    
    return next_q

@router.post("/{quiz_id}/answers", response_model=Dict[str, Any])
async def submit_answer(
    quiz_id: str,
    question_id: int = Body(...),
    selected: str = Body(...),
    time_taken_ms: Optional[int] = Body(None),
    confidence: Optional[int] = Body(None),
    db: AsyncSession = Depends(get_db)
):
    """Submit an answer for a question"""
    
    # Get quiz session
    query = select(QuizSession).where(QuizSession.id == uuid.UUID(quiz_id))
    result = await db.execute(query)
    session = result.scalar_one_or_none()
    
    if not session:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    # Get question and correct answer
    q_query = select(QuestionVersion, QuestionOption).join(
        QuestionOption, QuestionOption.question_version_id == QuestionVersion.id
    ).where(
        QuestionVersion.question_id == question_id,
        QuestionOption.is_correct == True
    )
    q_result = await db.execute(q_query)
    q_data = q_result.first()
    
    if not q_data:
        raise HTTPException(status_code=404, detail="Question not found")
    
    qv, correct_option = q_data
    is_correct = selected == correct_option.option_label
    
    # Save response
    response = UserResponse(
        quiz_id=uuid.UUID(quiz_id),
        user_id=session.user_id,
        question_id=question_id,
        version=qv.version,
        option_label=selected,
        is_correct=is_correct,
        time_taken_ms=time_taken_ms,
        confidence=confidence,
        created_at=datetime.utcnow()
    )
    db.add(response)
    
    # Update theta if adaptive
    if session.adaptive:
        # Get item parameters
        cal_query = select(ItemCalibration).where(
            ItemCalibration.question_id == question_id,
            ItemCalibration.version == qv.version,
            ItemCalibration.model == "3PL"
        )
        cal_result = await db.execute(cal_query)
        calibration = cal_result.scalar_one_or_none()
        
        if calibration:
            # Get current theta
            cached_session = await cache.get_session(quiz_id)
            if cached_session:
                theta = cached_session.get("theta", 0.0)
                responses = cached_session.get("responses", [])
                
                # Update theta using IRT
                new_theta, new_se = irt_engine.estimate_theta_eap(
                    responses + [{
                        "correct": is_correct,
                        "a": calibration.a or 1.0,
                        "b": calibration.b or 0.0,
                        "c": calibration.c or 0.0
                    }]
                )
                
                # Update cache
                cached_session["theta"] = new_theta
                cached_session["se"] = new_se
                cached_session["responses"].append({
                    "correct": is_correct,
                    "a": calibration.a or 1.0,
                    "b": calibration.b or 0.0,
                    "c": calibration.c or 0.0
                })
                await cache.set_session(quiz_id, cached_session)
                
                # Update user ability
                ability_query = select(UserAbility).where(
                    UserAbility.user_id == session.user_id,
                    UserAbility.topic_id == qv.topic_id
                )
                ability_result = await db.execute(ability_query)
                ability = ability_result.scalar_one_or_none()
                
                if ability:
                    ability.theta = new_theta
                    ability.theta_se = new_se
                    ability.n_responses += 1
                    ability.updated_at = datetime.utcnow()
                else:
                    ability = UserAbility(
                        user_id=session.user_id,
                        topic_id=qv.topic_id,
                        theta=new_theta,
                        theta_se=new_se,
                        n_responses=1,
                        updated_at=datetime.utcnow()
                    )
                    db.add(ability)
    
    await db.commit()
    
    return {
        "correct": is_correct,
        "correct_answer": correct_option.option_label,
        "explanation": correct_option.explanation_md,
        "rationale": qv.rationale_md
    }

@router.get("/{quiz_id}/results", response_model=Dict[str, Any])
async def get_quiz_results(
    quiz_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Get quiz results and analytics"""
    
    # Get quiz session
    query = select(QuizSession).where(QuizSession.id == uuid.UUID(quiz_id))
    result = await db.execute(query)
    session = result.scalar_one_or_none()
    
    if not session:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    # Get all responses
    resp_query = select(UserResponse).where(
        UserResponse.quiz_id == uuid.UUID(quiz_id)
    ).order_by(UserResponse.created_at)
    resp_result = await db.execute(resp_query)
    responses = resp_result.scalars().all()
    
    # Calculate statistics
    total = len(responses)
    correct = sum(1 for r in responses if r.is_correct)
    score = (correct / total * 100) if total > 0 else 0
    
    # Calculate time statistics
    total_time = sum(r.time_taken_ms or 0 for r in responses)
    avg_time = total_time / total if total > 0 else 0
    
    # Get theta progression if adaptive
    theta_progression = []
    if session.adaptive:
        cached_session = await cache.get_session(quiz_id)
        if cached_session:
            theta_progression = calculate_theta_progression(
                cached_session.get("responses", [])
            )
    
    # Topic-wise performance
    topic_performance = {}
    for response in responses:
        # Get question topic
        qv_query = select(QuestionVersion, Topic).join(
            Topic, Topic.id == QuestionVersion.topic_id
        ).where(
            QuestionVersion.question_id == response.question_id,
            QuestionVersion.version == response.version
        )
        qv_result = await db.execute(qv_query)
        qv_data = qv_result.first()
        
        if qv_data:
            qv, topic = qv_data
            topic_name = topic.name if topic else "General"
            
            if topic_name not in topic_performance:
                topic_performance[topic_name] = {"correct": 0, "total": 0}
            
            topic_performance[topic_name]["total"] += 1
            if response.is_correct:
                topic_performance[topic_name]["correct"] += 1
    
    return {
        "quiz_id": quiz_id,
        "mode": session.mode,
        "adaptive": session.adaptive,
        "completed": session.completed_at is not None,
        "score": score,
        "total_questions": total,
        "correct_answers": correct,
        "incorrect_answers": total - correct,
        "total_time_ms": total_time,
        "avg_time_ms": avg_time,
        "theta_progression": theta_progression,
        "topic_performance": topic_performance,
        "started_at": session.started_at.isoformat(),
        "completed_at": session.completed_at.isoformat() if session.completed_at else None
    }

# Helper functions
async def select_adaptive_question(
    db: AsyncSession,
    theta: float,
    topics: Optional[List[str]],
    difficulty: Optional[List[str]],
    exam_code: Optional[str],
    answered_ids: List[int]
) -> Optional[Dict[str, Any]]:
    """Select next question using adaptive algorithm"""
    
    # Build query for available questions
    query = select(
        QuestionVersion,
        Question,
        ItemCalibration
    ).join(
        Question, Question.id == QuestionVersion.question_id
    ).outerjoin(
        ItemCalibration, and_(
            ItemCalibration.question_id == QuestionVersion.question_id,
            ItemCalibration.version == QuestionVersion.version,
            ItemCalibration.model == "3PL"
        )
    ).where(
        QuestionVersion.state == "published",
        Question.is_deleted == False
    )
    
    # Apply filters
    if answered_ids:
        query = query.where(~Question.id.in_(answered_ids))
    
    if topics:
        topic_query = select(Topic.id).where(Topic.name.in_(topics))
        topic_result = await db.execute(topic_query)
        topic_ids = [t[0] for t in topic_result.fetchall()]
        if topic_ids:
            query = query.where(QuestionVersion.topic_id.in_(topic_ids))
    
    if difficulty:
        query = query.where(QuestionVersion.difficulty_label.in_(difficulty))
    
    # Execute query
    result = await db.execute(query)
    available = result.all()
    
    if not available:
        return None
    
    # Calculate information for each question
    questions_with_info = []
    for qv, q, cal in available:
        if cal and cal.a and cal.b:
            # Use calibrated parameters
            a, b, c = cal.a, cal.b, cal.c or 0.0
        else:
            # Use default parameters based on difficulty
            difficulty_params = {
                "very_easy": {"a": 1.0, "b": -2.0, "c": 0.1},
                "easy": {"a": 1.0, "b": -1.0, "c": 0.15},
                "medium": {"a": 1.0, "b": 0.0, "c": 0.2},
                "hard": {"a": 1.0, "b": 1.0, "c": 0.2},
                "very_hard": {"a": 1.0, "b": 2.0, "c": 0.25}
            }
            params = difficulty_params.get(
                qv.difficulty_label or "medium",
                difficulty_params["medium"]
            )
            a, b, c = params["a"], params["b"], params["c"]
        
        # Calculate Fisher information at current theta
        info = irt_engine.information_3pl(theta, a, b, c)
        
        # Apply exposure control
        can_serve = await cache.can_serve(q.id, qv.version)
        if can_serve:
            questions_with_info.append({
                "id": q.id,
                "version": qv.version,
                "info": info,
                "a": a,
                "b": b,
                "c": c,
                "qv": qv,
                "q": q
            })
    
    if not questions_with_info:
        return None
    
    # Sort by information and select from top candidates
    questions_with_info.sort(key=lambda x: x["info"], reverse=True)
    
    # Add randomization to avoid always selecting same questions
    top_n = min(5, len(questions_with_info))
    selected = random.choice(questions_with_info[:top_n])
    
    # Update exposure count
    await cache.bump_exposure(selected["id"], selected["version"])
    
    # Get options
    opt_query = select(QuestionOption).where(
        QuestionOption.question_version_id == selected["qv"].id
    ).order_by(QuestionOption.option_label)
    opt_result = await db.execute(opt_query)
    options = opt_result.scalars().all()
    
    return {
        "id": selected["id"],
        "version": selected["version"],
        "stem": selected["qv"].stem_md,
        "lead_in": selected["qv"].lead_in,
        "options": [
            {
                "label": opt.option_label,
                "text": opt.option_text_md
            }
            for opt in options
        ],
        "parameters": {
            "a": selected["a"],
            "b": selected["b"],
            "c": selected["c"]
        }
    }

async def select_random_questions(
    db: AsyncSession,
    num: int,
    topics: Optional[List[str]],
    difficulty: Optional[List[str]],
    exam_code: Optional[str]
) -> List[Dict[str, Any]]:
    """Select random questions based on criteria"""
    
    query = select(
        QuestionVersion,
        Question
    ).join(
        Question, Question.id == QuestionVersion.question_id
    ).where(
        QuestionVersion.state == "published",
        Question.is_deleted == False
    )
    
    # Apply filters
    if topics:
        topic_query = select(Topic.id).where(Topic.name.in_(topics))
        topic_result = await db.execute(topic_query)
        topic_ids = [t[0] for t in topic_result.fetchall()]
        if topic_ids:
            query = query.where(QuestionVersion.topic_id.in_(topic_ids))
    
    if difficulty:
        query = query.where(QuestionVersion.difficulty_label.in_(difficulty))
    
    # Get all matching questions
    result = await db.execute(query)
    all_questions = result.all()
    
    # Randomly select requested number
    selected = random.sample(all_questions, min(num, len(all_questions)))
    
    return [
        {
            "id": q.id,
            "version": qv.version
        }
        for qv, q in selected
    ]

def calculate_theta_progression(responses: List[Dict]) -> List[float]:
    """Calculate theta progression through the test"""
    progression = []
    theta = 0.0
    
    for i, resp in enumerate(responses):
        # Simple EAP update
        p = irt_engine.probability_3pl(
            theta, 
            resp.get("a", 1.0),
            resp.get("b", 0.0),
            resp.get("c", 0.0)
        )
        score = 1 if resp["correct"] else 0
        
        # Update theta
        residual = score - p
        info = irt_engine.information_3pl(
            theta,
            resp.get("a", 1.0),
            resp.get("b", 0.0),
            resp.get("c", 0.0)
        )
        
        adjustment = residual / max(info, 0.1)
        theta = theta + adjustment * 0.5  # Damping factor
        theta = max(-3, min(3, theta))  # Bound theta
        
        progression.append(theta)
    
    return progression