from sqlalchemy import (
    BigInteger, Integer, String, Text, Boolean, Float, 
    ForeignKey, JSON, DateTime, UniqueConstraint, Index,
    CheckConstraint, Enum as SQLEnum, func
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB, ARRAY, TSVECTOR
from datetime import datetime
from typing import Optional, List, Dict, Any
import uuid
import enum
from app.core.database import Base

class QuestionState(str, enum.Enum):
    DRAFT = "draft"
    IN_REVIEW = "in_review"
    APPROVED = "approved"
    PUBLISHED = "published"
    ARCHIVED = "archived"

class QuizMode(str, enum.Enum):
    TUTOR = "tutor"
    EXAM = "exam"
    PRACTICE = "practice"
    DIAGNOSTIC = "diagnostic"

class DifficultyLevel(str, enum.Enum):
    VERY_EASY = "very_easy"
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    VERY_HARD = "very_hard"

# ========== Content Models ==========

class Topic(Base):
    __tablename__ = "topics"
    __table_args__ = (
        Index("idx_topics_tenant", "tenant_id"),
        Index("idx_topics_parent", "parent_id"),
        Index("idx_topics_blueprint", "blueprint_code"),
    )
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    tenant_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    parent_id: Mapped[Optional[int]] = mapped_column(
        BigInteger, ForeignKey("topics.id", ondelete="CASCADE")
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    blueprint_code: Mapped[Optional[str]] = mapped_column(String(50))
    description: Mapped[Optional[str]] = mapped_column(Text)
    weight: Mapped[float] = mapped_column(Float, default=1.0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    metadata: Mapped[Dict[str, Any]] = mapped_column(JSONB, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now()
    )
    
    # Relationships
    children: Mapped[List["Topic"]] = relationship(
        back_populates="parent", cascade="all, delete-orphan"
    )
    parent: Mapped[Optional["Topic"]] = relationship(
        back_populates="children", remote_side=[id]
    )
    questions: Mapped[List["QuestionVersion"]] = relationship(
        back_populates="topic"
    )

class Question(Base):
    __tablename__ = "questions"
    __table_args__ = (
        Index("idx_questions_tenant", "tenant_id"),
        Index("idx_questions_external_ref", "external_ref"),
        Index("idx_questions_created_by", "created_by"),
        Index("idx_questions_created_at", "created_at"),
        UniqueConstraint("tenant_id", "external_ref", name="uq_questions_external_ref"),
    )
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    tenant_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    external_ref: Mapped[Optional[str]] = mapped_column(String(100))
    created_by: Mapped[str] = mapped_column(String(255), nullable=False)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    metadata: Mapped[Dict[str, Any]] = mapped_column(JSONB, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    
    # Relationships
    versions: Mapped[List["QuestionVersion"]] = relationship(
        back_populates="question", cascade="all, delete-orphan"
    )
    publications: Mapped[List["QuestionPublication"]] = relationship(
        back_populates="question", cascade="all, delete-orphan"
    )

class QuestionVersion(Base):
    __tablename__ = "question_versions"
    __table_args__ = (
        Index("idx_qv_question", "question_id"),
        Index("idx_qv_topic", "topic_id"),
        Index("idx_qv_state", "state"),
        Index("idx_qv_version", "version"),
        Index("idx_qv_search", "search_vector", postgresql_using="gin"),
        UniqueConstraint("question_id", "version", name="uq_question_version"),
    )
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    question_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("questions.id", ondelete="CASCADE"), nullable=False
    )
    version: Mapped[int] = mapped_column(Integer, nullable=False)
    state: Mapped[QuestionState] = mapped_column(
        SQLEnum(QuestionState), nullable=False, default=QuestionState.DRAFT
    )
    stem_md: Mapped[str] = mapped_column(Text, nullable=False)
    lead_in: Mapped[str] = mapped_column(Text, nullable=False)
    rationale_md: Mapped[str] = mapped_column(Text, nullable=False)
    difficulty_label: Mapped[Optional[DifficultyLevel]] = mapped_column(
        SQLEnum(DifficultyLevel)
    )
    bloom_level: Mapped[Optional[int]] = mapped_column(Integer)
    topic_id: Mapped[Optional[int]] = mapped_column(
        BigInteger, ForeignKey("topics.id", ondelete="SET NULL")
    )
    tags: Mapped[List[str]] = mapped_column(ARRAY(String), default=list)
    assets: Mapped[List[Dict]] = mapped_column(JSONB, default=list)
    references: Mapped[List[Dict]] = mapped_column(JSONB, default=list)
    search_vector: Mapped[Optional[str]] = mapped_column(TSVECTOR)
    embedding: Mapped[Optional[List[float]]] = mapped_column(ARRAY(Float))
    metadata: Mapped[Dict[str, Any]] = mapped_column(JSONB, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now()
    )
    reviewed_by: Mapped[Optional[str]] = mapped_column(String(255))
    reviewed_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    
    # Relationships
    question: Mapped["Question"] = relationship(back_populates="versions")
    topic: Mapped[Optional["Topic"]] = relationship(back_populates="questions")
    options: Mapped[List["QuestionOption"]] = relationship(
        back_populates="question_version", cascade="all, delete-orphan"
    )
    calibrations: Mapped[List["ItemCalibration"]] = relationship(
        back_populates="question_version"
    )

class QuestionOption(Base):
    __tablename__ = "question_options"
    __table_args__ = (
        Index("idx_qo_question_version", "question_version_id"),
        UniqueConstraint(
            "question_version_id", "option_label", 
            name="uq_question_option"
        ),
    )
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    question_version_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("question_versions.id", ondelete="CASCADE"), 
        nullable=False
    )
    option_label: Mapped[str] = mapped_column(String(1), nullable=False)
    option_text_md: Mapped[str] = mapped_column(Text, nullable=False)
    is_correct: Mapped[bool] = mapped_column(Boolean, nullable=False)
    explanation_md: Mapped[Optional[str]] = mapped_column(Text)
    metadata: Mapped[Dict[str, Any]] = mapped_column(JSONB, default=dict)
    
    # Relationships
    question_version: Mapped["QuestionVersion"] = relationship(
        back_populates="options"
    )

class QuestionPublication(Base):
    __tablename__ = "question_publications"
    __table_args__ = (
        Index("idx_qp_question", "question_id"),
        Index("idx_qp_exam_code", "exam_code"),
        Index("idx_qp_tenant", "tenant_id"),
        UniqueConstraint(
            "question_id", "exam_code", 
            name="uq_question_publication"
        ),
    )
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    question_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("questions.id", ondelete="CASCADE"), 
        nullable=False
    )
    live_version: Mapped[int] = mapped_column(Integer, nullable=False)
    exam_code: Mapped[str] = mapped_column(String(50), nullable=False)
    tenant_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    published_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    published_by: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    metadata: Mapped[Dict[str, Any]] = mapped_column(JSONB, default=dict)
    
    # Relationships
    question: Mapped["Question"] = relationship(back_populates="publications")

# ========== Delivery Models ==========

class QuizSession(Base):
    __tablename__ = "quiz_sessions"
    __table_args__ = (
        Index("idx_qs_user", "user_id"),
        Index("idx_qs_tenant", "tenant_id"),
        Index("idx_qs_started", "started_at"),
        Index("idx_qs_mode", "mode"),
        CheckConstraint(
            "expires_at > started_at", 
            name="ck_quiz_session_expires"
        ),
    )
    
    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[str] = mapped_column(String(255), nullable=False)
    tenant_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    mode: Mapped[QuizMode] = mapped_column(
        SQLEnum(QuizMode), nullable=False, default=QuizMode.PRACTICE
    )
    adaptive: Mapped[bool] = mapped_column(Boolean, default=False)
    exam_code: Mapped[Optional[str]] = mapped_column(String(50))
    config: Mapped[Dict[str, Any]] = mapped_column(JSONB, default=dict)
    started_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    score: Mapped[Optional[float]] = mapped_column(Float)
    metadata: Mapped[Dict[str, Any]] = mapped_column(JSONB, default=dict)
    
    # Relationships
    items: Mapped[List["QuizItem"]] = relationship(
        back_populates="session", cascade="all, delete-orphan"
    )
    responses: Mapped[List["UserResponse"]] = relationship(
        back_populates="session", cascade="all, delete-orphan"
    )

class QuizItem(Base):
    __tablename__ = "quiz_items"
    __table_args__ = (
        Index("idx_qi_quiz", "quiz_id"),
        Index("idx_qi_question", "question_id"),
        UniqueConstraint("quiz_id", "position", name="uq_quiz_item_position"),
    )
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    quiz_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), 
        ForeignKey("quiz_sessions.id", ondelete="CASCADE"), 
        nullable=False
    )
    question_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    version: Mapped[int] = mapped_column(Integer, nullable=False)
    position: Mapped[int] = mapped_column(Integer, nullable=False)
    served_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    metadata: Mapped[Dict[str, Any]] = mapped_column(JSONB, default=dict)
    
    # Relationships
    session: Mapped["QuizSession"] = relationship(back_populates="items")

class UserResponse(Base):
    __tablename__ = "user_responses"
    __table_args__ = (
        Index("idx_ur_quiz", "quiz_id"),
        Index("idx_ur_user", "user_id"),
        Index("idx_ur_question", "question_id", "version"),
        Index("idx_ur_created", "created_at"),
        UniqueConstraint(
            "quiz_id", "question_id", 
            name="uq_user_response"
        ),
    )
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    quiz_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), 
        ForeignKey("quiz_sessions.id", ondelete="CASCADE"), 
        nullable=False
    )
    user_id: Mapped[str] = mapped_column(String(255), nullable=False)
    question_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    version: Mapped[int] = mapped_column(Integer, nullable=False)
    option_label: Mapped[str] = mapped_column(String(1), nullable=False)
    is_correct: Mapped[bool] = mapped_column(Boolean, nullable=False)
    time_taken_ms: Mapped[Optional[int]] = mapped_column(Integer)
    confidence: Mapped[Optional[int]] = mapped_column(Integer)
    metadata: Mapped[Dict[str, Any]] = mapped_column(JSONB, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    
    # Relationships
    session: Mapped["QuizSession"] = relationship(back_populates="responses")

# ========== Analytics Models ==========

class ItemCalibration(Base):
    __tablename__ = "item_calibration"
    __table_args__ = (
        Index("idx_ic_question", "question_id", "version"),
        Index("idx_ic_model", "model"),
        Index("idx_ic_calibrated", "calibrated_at"),
    )
    
    question_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    version: Mapped[int] = mapped_column(Integer, primary_key=True)
    model: Mapped[str] = mapped_column(String(10), primary_key=True)
    a: Mapped[Optional[float]] = mapped_column(Float)  # Discrimination
    b: Mapped[Optional[float]] = mapped_column(Float)  # Difficulty
    c: Mapped[Optional[float]] = mapped_column(Float)  # Guessing
    se_a: Mapped[Optional[float]] = mapped_column(Float)  # Standard errors
    se_b: Mapped[Optional[float]] = mapped_column(Float)
    se_c: Mapped[Optional[float]] = mapped_column(Float)
    n_respondents: Mapped[Optional[int]] = mapped_column(Integer)
    fit_statistics: Mapped[Dict[str, Any]] = mapped_column(JSONB, default=dict)
    calibrated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    
    # Relationships
    question_version: Mapped["QuestionVersion"] = relationship(
        foreign_keys="[ItemCalibration.question_id, ItemCalibration.version]",
        primaryjoin="and_(ItemCalibration.question_id==QuestionVersion.question_id, "
                   "ItemCalibration.version==QuestionVersion.version)",
        viewonly=True,
    )

class ItemExposureControl(Base):
    __tablename__ = "item_exposure_control"
    __table_args__ = (
        Index("idx_iec_question", "question_id", "version"),
        Index("idx_iec_updated", "updated_at"),
    )
    
    question_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    version: Mapped[int] = mapped_column(Integer, primary_key=True)
    sh_p: Mapped[float] = mapped_column(Float, default=1.0, nullable=False)
    exposure_count: Mapped[int] = mapped_column(Integer, default=0)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now()
    )

class UserAbility(Base):
    __tablename__ = "user_abilities"
    __table_args__ = (
        Index("idx_ua_user", "user_id"),
        Index("idx_ua_topic", "topic_id"),
        Index("idx_ua_updated", "updated_at"),
        UniqueConstraint("user_id", "topic_id", name="uq_user_ability"),
    )
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    user_id: Mapped[str] = mapped_column(String(255), nullable=False)
    topic_id: Mapped[Optional[int]] = mapped_column(BigInteger)  # NULL = global
    theta: Mapped[float] = mapped_column(Float, default=0.0)
    theta_se: Mapped[float] = mapped_column(Float, default=1.0)
    n_responses: Mapped[int] = mapped_column(Integer, default=0)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now()
    )

# ========== Governance Models ==========

class FeatureFlag(Base):
    __tablename__ = "feature_flags"
    __table_args__ = (
        Index("idx_ff_key", "key"),
    )
    
    key: Mapped[str] = mapped_column(String(100), primary_key=True)
    enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    value_json: Mapped[Dict[str, Any]] = mapped_column(JSONB, default=dict)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now()
    )

class CohortAssignment(Base):
    __tablename__ = "cohort_assignments"
    __table_args__ = (
        Index("idx_ca_user", "user_id"),
        Index("idx_ca_cohort", "cohort_key"),
    )
    
    user_id: Mapped[str] = mapped_column(String(255), primary_key=True)
    cohort_key: Mapped[str] = mapped_column(String(100), primary_key=True)
    cohort_value: Mapped[str] = mapped_column(String(255), nullable=False)
    assigned_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())

class CalibrationRun(Base):
    __tablename__ = "calibration_runs"
    __table_args__ = (
        Index("idx_cr_exam", "exam_code"),
        Index("idx_cr_status", "status"),
        Index("idx_cr_created", "created_at"),
    )
    
    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    exam_code: Mapped[str] = mapped_column(String(50), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False)
    params: Mapped[Dict[str, Any]] = mapped_column(JSONB, nullable=False)
    history: Mapped[List[Dict]] = mapped_column(JSONB, default=list)
    result: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB)
    error: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    started_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    finished_at: Mapped[Optional[datetime]] = mapped_column(DateTime)

class AuditLog(Base):
    __tablename__ = "audit_logs"
    __table_args__ = (
        Index("idx_al_user", "user_id"),
        Index("idx_al_entity", "entity_type", "entity_id"),
        Index("idx_al_created", "created_at"),
    )
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    user_id: Mapped[str] = mapped_column(String(255), nullable=False)
    action: Mapped[str] = mapped_column(String(50), nullable=False)
    entity_type: Mapped[str] = mapped_column(String(50), nullable=False)
    entity_id: Mapped[str] = mapped_column(String(255), nullable=False)
    changes: Mapped[Dict[str, Any]] = mapped_column(JSONB, default=dict)
    metadata: Mapped[Dict[str, Any]] = mapped_column(JSONB, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())