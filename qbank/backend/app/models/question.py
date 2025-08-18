"""
Database models for QBank system
"""

from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, JSON, ForeignKey, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Question(Base):
    """Question model with IRT parameters"""
    __tablename__ = "questions"
    
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    subject = Column(String(100), nullable=False, index=True)
    topic = Column(String(100), nullable=False, index=True)
    difficulty_level = Column(String(20), nullable=False, index=True)
    
    # IRT Parameters
    discrimination = Column(Float, default=1.0)  # a parameter
    difficulty = Column(Float, default=0.0)  # b parameter
    guessing = Column(Float, default=0.25)  # c parameter
    
    # Sympson-Hetter Exposure Control
    exposure_rate = Column(Float, default=0.0)
    exposure_count = Column(Integer, default=0)
    selection_probability = Column(Float, default=1.0)
    last_exposed = Column(DateTime, nullable=True)
    
    # Question metadata
    question_type = Column(String(50), nullable=False)  # multiple_choice, true_false, etc.
    options = Column(JSON, nullable=True)  # For multiple choice questions
    correct_answer = Column(String(500), nullable=False)
    explanation = Column(Text, nullable=True)
    
    # Statistics
    total_responses = Column(Integer, default=0)
    correct_responses = Column(Integer, default=0)
    average_response_time = Column(Float, default=0.0)
    
    # Calibration metadata
    last_calibrated = Column(DateTime, nullable=True)
    calibration_sample_size = Column(Integer, default=0)
    standard_error_a = Column(Float, nullable=True)
    standard_error_b = Column(Float, nullable=True)
    standard_error_c = Column(Float, nullable=True)
    
    # Content tags
    tags = Column(JSON, default=list)
    cognitive_level = Column(String(50), nullable=True)  # Bloom's taxonomy
    
    # Administrative
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    is_active = Column(Boolean, default=True)
    review_status = Column(String(20), default="approved")
    
    # Relationships
    responses = relationship("Response", back_populates="question")
    
    # Indexes
    __table_args__ = (
        Index('idx_subject_topic', 'subject', 'topic'),
        Index('idx_difficulty', 'difficulty'),
        Index('idx_exposure', 'exposure_rate'),
        Index('idx_active_subject', 'is_active', 'subject'),
    )

class TestSession(Base):
    """Adaptive testing session"""
    __tablename__ = "test_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(100), nullable=False, index=True)
    session_token = Column(String(200), unique=True, index=True)
    
    # Test configuration
    test_type = Column(String(50), nullable=False)
    subject = Column(String(100), nullable=False)
    target_questions = Column(Integer, default=20)
    
    # IRT estimates
    ability_estimate = Column(Float, default=0.0)
    ability_se = Column(Float, default=1.0)  # Standard error
    
    # Session state
    status = Column(String(20), default="active")  # active, completed, abandoned
    questions_answered = Column(Integer, default=0)
    correct_answers = Column(Integer, default=0)
    
    # Timing
    started_at = Column(DateTime, default=func.now())
    completed_at = Column(DateTime, nullable=True)
    last_activity = Column(DateTime, default=func.now())
    total_time_seconds = Column(Integer, default=0)
    
    # Session data
    ability_history = Column(JSON, default=list)  # Track ability estimates over time
    question_sequence = Column(JSON, default=list)  # Order of questions presented
    
    # Relationships
    responses = relationship("Response", back_populates="session")

class Response(Base):
    """Student responses to questions"""
    __tablename__ = "responses"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("test_sessions.id"))
    question_id = Column(Integer, ForeignKey("questions.id"))
    user_id = Column(String(100), nullable=False, index=True)
    
    # Response data
    given_answer = Column(String(500), nullable=False)
    is_correct = Column(Boolean, nullable=False)
    response_time = Column(Float, nullable=False)  # in seconds
    
    # IRT data at time of response
    ability_before = Column(Float, nullable=False)
    ability_after = Column(Float, nullable=False)
    information_value = Column(Float, nullable=True)  # Fisher information
    
    # Metadata
    created_at = Column(DateTime, default=func.now())
    flagged_for_review = Column(Boolean, default=False)
    
    # Relationships
    session = relationship("TestSession", back_populates="responses")
    question = relationship("Question", back_populates="responses")
    
    # Indexes
    __table_args__ = (
        Index('idx_session_question', 'session_id', 'question_id'),
        Index('idx_user_created', 'user_id', 'created_at'),
    )

class CalibrationRun(Base):
    """Track calibration runs for audit and analysis"""
    __tablename__ = "calibration_runs"
    
    id = Column(Integer, primary_key=True, index=True)
    run_id = Column(String(100), unique=True, index=True)
    
    # Calibration details
    started_at = Column(DateTime, default=func.now())
    completed_at = Column(DateTime, nullable=True)
    status = Column(String(20), default="running")  # running, completed, failed
    
    # Statistics
    questions_calibrated = Column(Integer, default=0)
    total_responses_used = Column(Integer, default=0)
    convergence_iterations = Column(Integer, nullable=True)
    log_likelihood = Column(Float, nullable=True)
    
    # Parameters
    calibration_method = Column(String(50), nullable=False)
    calibration_config = Column(JSON, nullable=True)
    
    # Results summary
    results_summary = Column(JSON, nullable=True)
    error_message = Column(Text, nullable=True)

class ExposureControl(Base):
    """Sympson-Hetter exposure control parameters"""
    __tablename__ = "exposure_control"
    
    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("questions.id"), unique=True)
    
    # Sympson-Hetter parameters
    target_exposure = Column(Float, default=0.25)
    current_exposure = Column(Float, default=0.0)
    selection_parameter = Column(Float, default=1.0)
    
    # Control statistics
    total_eligible = Column(Integer, default=0)  # Times question was eligible
    total_administered = Column(Integer, default=0)  # Times actually given
    
    # Adaptive control
    control_parameter = Column(Float, default=1.0)
    last_updated = Column(DateTime, default=func.now())
    
    # Phase tracking
    phase = Column(String(20), default="initial")  # initial, operational, fade
    phase_iterations = Column(Integer, default=0)

class ItemBank(Base):
    """Item bank metadata and organization"""
    __tablename__ = "item_banks"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    
    # Bank configuration
    subject = Column(String(100), nullable=False)
    grade_level = Column(String(50), nullable=True)
    test_type = Column(String(50), nullable=True)
    
    # Statistics
    total_items = Column(Integer, default=0)
    active_items = Column(Integer, default=0)
    average_difficulty = Column(Float, nullable=True)
    average_discrimination = Column(Float, nullable=True)
    
    # Metadata
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    created_by = Column(String(100), nullable=True)
    
    # Configuration
    config = Column(JSON, default=dict)

# Database initialization
async def init_db():
    """Initialize database with async support"""
    # This would normally connect to PostgreSQL
    # For now, using SQLite for demonstration
    engine = create_async_engine(
        "sqlite+aiosqlite:///./qbank.db",
        echo=True,
    )
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    return engine

# Session factory
async def get_session():
    """Get database session"""
    engine = await init_db()
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session