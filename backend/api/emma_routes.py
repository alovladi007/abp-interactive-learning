"""
EMMA API Routes
FastAPI endpoints for EMMA AI STEM Tutor
"""

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
import logging
from uuid import uuid4

from services.emma_core import (
    EMMACore,
    Problem,
    ProblemType,
    DifficultyLevel,
    QuizQuestion,
    Solution
)

logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/api/emma", tags=["EMMA"])

# Initialize EMMA
emma_instance = None


def get_emma():
    """Dependency to get EMMA instance"""
    global emma_instance
    if emma_instance is None:
        emma_instance = EMMACore()
    return emma_instance


# Pydantic models for API
class ProblemRequest(BaseModel):
    question: str = Field(..., description="The problem to solve")
    problem_type: str = Field(..., description="Type of problem (algebra, calculus, etc.)")
    difficulty: str = Field(default="intermediate", description="Difficulty level")
    tags: List[str] = Field(default_factory=list, description="Problem tags")
    user_id: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "question": "x**2 - 5*x + 6",
                "problem_type": "algebra",
                "difficulty": "beginner",
                "tags": ["quadratic", "factoring"]
            }
        }


class SolutionResponse(BaseModel):
    solution_id: str
    problem: Dict[str, Any]
    steps: List[Dict[str, str]]
    final_answer: str
    latex_answer: str
    verification: Optional[str]
    visualizations: List[str]
    explanation: str
    computation_time_ms: int


class ExplainRequest(BaseModel):
    question: str
    answer: str
    detail_level: str = Field(default="detailed", description="brief, detailed, or expert")


class VisualizeRequest(BaseModel):
    expression: str
    variable: str = "x"
    x_min: float = -10
    x_max: float = 10
    plot_type: str = Field(default="function", description="function, derivative, or both")


class QuizRequest(BaseModel):
    topic: str
    difficulty: str = "intermediate"
    num_questions: int = Field(default=10, ge=1, le=50)


class AnswerSubmission(BaseModel):
    user_id: str
    question_id: str
    selected_answer: str
    time_taken_seconds: int


class StudyPlanRequest(BaseModel):
    user_id: str
    topics: Optional[List[str]] = None
    target_hours_per_week: int = 5


# Endpoints
@router.post("/solve", response_model=SolutionResponse)
async def solve_problem(
    request: ProblemRequest,
    emma: EMMACore = Depends(get_emma)
):
    """
    Solve a STEM problem with step-by-step solution

    Returns detailed solution with steps, explanations, and visualizations
    """
    try:
        # Convert string types to enums
        try:
            problem_type = ProblemType[request.problem_type.upper()]
        except KeyError:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid problem type. Must be one of: {', '.join([pt.value for pt in ProblemType])}"
            )

        try:
            difficulty = DifficultyLevel[request.difficulty.upper()]
        except KeyError:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid difficulty. Must be one of: {', '.join([dl.value for dl in DifficultyLevel])}"
            )

        # Create problem
        problem = Problem(
            question=request.question,
            problem_type=problem_type,
            difficulty=difficulty,
            tags=request.tags
        )

        # Solve
        logger.info(f"Solving {problem_type.value} problem: {request.question[:50]}...")
        solution = await emma.solve_problem(problem)

        # Create response
        return SolutionResponse(
            solution_id=str(uuid4()),
            problem={
                "question": solution.problem.question,
                "type": solution.problem.problem_type.value,
                "difficulty": solution.problem.difficulty.value,
                "tags": solution.problem.tags
            },
            steps=solution.steps,
            final_answer=solution.final_answer,
            latex_answer=solution.latex_answer,
            verification=solution.verification,
            visualizations=solution.visualizations,
            explanation=solution.explanation,
            computation_time_ms=solution.computation_time_ms
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error solving problem: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error while solving problem")


@router.post("/explain")
async def explain_solution(
    request: ExplainRequest,
    emma: EMMACore = Depends(get_emma)
):
    """
    Get detailed natural language explanation of a solution
    """
    try:
        # Create a problem from the question
        problem = Problem(
            question=request.question,
            problem_type=ProblemType.ALGEBRA,  # Default
            difficulty=DifficultyLevel.INTERMEDIATE,
            tags=[]
        )

        # Solve to get explanation
        solution = await emma.solve_problem(problem)

        # Generate additional explanation if needed
        explanation = solution.explanation
        if request.detail_level == "expert":
            explanation = emma.solver.generate_explanation(solution)

        return {
            "question": request.question,
            "answer": request.answer,
            "explanation": explanation,
            "steps": solution.steps if request.detail_level != "brief" else [],
            "key_concepts": solution.problem.tags
        }

    except Exception as e:
        logger.error(f"Error explaining solution: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate explanation")


@router.post("/visualize")
async def visualize_expression(
    request: VisualizeRequest,
    emma: EMMACore = Depends(get_emma)
):
    """
    Generate visualization for mathematical expression
    """
    try:
        if request.plot_type == "function":
            plot = emma.visualizer.plot_function(
                request.expression,
                variable=request.variable,
                x_range=(request.x_min, request.x_max)
            )
        elif request.plot_type == "derivative":
            plot = emma.visualizer.plot_derivative_comparison(
                request.expression,
                x_range=(request.x_min, request.x_max)
            )
        elif request.plot_type == "both":
            plot = emma.visualizer.plot_derivative_comparison(
                request.expression,
                x_range=(request.x_min, request.x_max)
            )
        else:
            raise HTTPException(status_code=400, detail="Invalid plot_type")

        return {
            "expression": request.expression,
            "plot_type": request.plot_type,
            "image": plot
        }

    except Exception as e:
        logger.error(f"Error creating visualization: {e}")
        raise HTTPException(status_code=500, detail="Failed to create visualization")


@router.get("/quiz/{topic}")
async def get_quiz(
    topic: str,
    difficulty: str = "intermediate",
    num_questions: int = 10,
    emma: EMMACore = Depends(get_emma)
):
    """
    Generate quiz questions on a specific topic
    """
    try:
        # Convert difficulty
        try:
            diff_level = DifficultyLevel[difficulty.upper()]
        except KeyError:
            raise HTTPException(status_code=400, detail="Invalid difficulty level")

        # Generate quiz
        questions = emma.generate_quiz(topic, diff_level, num_questions)

        return {
            "topic": topic,
            "difficulty": difficulty,
            "num_questions": len(questions),
            "questions": [
                {
                    "question_id": q.question_id,
                    "question": q.question,
                    "options": [q.correct_answer] + q.distractors,
                    "topic": q.topic,
                    "difficulty": q.difficulty.value
                }
                for q in questions
            ]
        }

    except Exception as e:
        logger.error(f"Error generating quiz: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate quiz")


@router.post("/answer")
async def submit_answer(
    submission: AnswerSubmission,
    emma: EMMACore = Depends(get_emma)
):
    """
    Submit quiz answer and get feedback with spaced repetition update
    """
    try:
        # Get the question
        if submission.question_id not in emma.srs.questions_db:
            raise HTTPException(status_code=404, detail="Question not found")

        question = emma.srs.questions_db[submission.question_id]

        # Check if correct
        is_correct = submission.selected_answer.strip().lower() == question.correct_answer.strip().lower()

        # Calculate quality score (0-5)
        # Based on correctness and time taken
        if is_correct:
            if submission.time_taken_seconds < 10:
                quality = 5  # Perfect recall
            elif submission.time_taken_seconds < 30:
                quality = 4  # Good recall
            else:
                quality = 3  # Acceptable
        else:
            quality = 0  # Complete blackout

        # Update spaced repetition
        updated_question = emma.srs.record_answer(submission.question_id, quality)

        return {
            "correct": is_correct,
            "correct_answer": question.correct_answer,
            "explanation": question.explanation,
            "quality_score": quality,
            "next_review": updated_question.next_review.isoformat() if updated_question.next_review else None,
            "interval_days": updated_question.interval_days,
            "repetitions": updated_question.repetitions,
            "ease_factor": updated_question.ease_factor
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error submitting answer: {e}")
        raise HTTPException(status_code=500, detail="Failed to process answer")


@router.get("/progress/{user_id}")
async def get_progress(
    user_id: str,
    emma: EMMACore = Depends(get_emma)
):
    """
    Get user's learning progress and statistics
    """
    try:
        study_plan = emma.get_study_plan(user_id)
        stats = emma.srs.get_statistics()

        return {
            "user_id": user_id,
            "statistics": stats,
            "due_questions": study_plan["due_questions"],
            "next_review": study_plan["next_review"].isoformat() if study_plan["next_review"] else None,
            "recommended_topics": study_plan["recommended_topics"],
            "mastery_percentage": stats["mastery_percentage"]
        }

    except Exception as e:
        logger.error(f"Error getting progress: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve progress")


@router.post("/study-plan")
async def create_study_plan(
    request: StudyPlanRequest,
    emma: EMMACore = Depends(get_emma)
):
    """
    Generate personalized study plan based on user progress
    """
    try:
        study_plan = emma.get_study_plan(request.user_id)
        stats = emma.srs.get_statistics()

        # Calculate daily study time
        daily_minutes = (request.target_hours_per_week * 60) // 7

        # Get due questions
        due_questions = emma.srs.get_due_questions()

        return {
            "user_id": request.user_id,
            "target_hours_per_week": request.target_hours_per_week,
            "daily_minutes": daily_minutes,
            "current_statistics": stats,
            "due_now": len(due_questions),
            "recommended_daily_questions": max(10, len(due_questions) // 7),
            "topics_to_focus": study_plan["recommended_topics"],
            "next_milestone": {
                "type": "mastery" if stats["mastery_percentage"] < 80 else "review",
                "target": "80% mastery" if stats["mastery_percentage"] < 80 else "Maintain mastery",
                "progress": f"{stats['mastery_percentage']:.1f}%"
            }
        }

    except Exception as e:
        logger.error(f"Error creating study plan: {e}")
        raise HTTPException(status_code=500, detail="Failed to create study plan")


@router.get("/topics")
async def list_topics():
    """
    Get list of available topics and problem types
    """
    return {
        "problem_types": [pt.value for pt in ProblemType],
        "difficulty_levels": [dl.value for dl in DifficultyLevel],
        "topics": {
            "algebra": ["equations", "polynomials", "inequalities", "systems", "factoring"],
            "calculus": ["derivatives", "integrals", "limits", "series", "optimization"],
            "linear_algebra": ["matrices", "vectors", "eigenvalues", "transformations"],
            "physics": ["kinematics", "dynamics", "energy", "momentum", "waves"],
            "chemistry": ["stoichiometry", "equilibrium", "kinetics", "thermodynamics"],
            "statistics": ["probability", "distributions", "hypothesis_testing", "regression"]
        }
    }


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "EMMA"}

