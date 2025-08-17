"""Enrollment and progress tracking models for EUREKA marketplace"""
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, JSON, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
from typing import Dict
from enum import Enum

from config.database import Base

class EnrollmentStatus(str, Enum):
    ACTIVE = "active"
    COMPLETED = "completed"
    EXPIRED = "expired"
    SUSPENDED = "suspended"
    REFUNDED = "refunded"

class PaymentStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"

class Enrollment(Base):
    __tablename__ = "enrollments"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    
    # Enrollment Details
    status = Column(String(20), default=EnrollmentStatus.ACTIVE)
    enrolled_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True))
    expires_at = Column(DateTime(timezone=True))
    last_accessed = Column(DateTime(timezone=True))
    
    # Progress Tracking
    progress_percentage = Column(Float, default=0.0)
    completed_lessons = Column(Integer, default=0)
    total_time_spent = Column(Integer, default=0)  # in minutes
    current_module_id = Column(Integer, ForeignKey("course_modules.id"))
    current_lesson_id = Column(Integer, ForeignKey("lessons.id"))
    
    # Payment Information
    payment_status = Column(String(20), default=PaymentStatus.PENDING)
    payment_amount = Column(Float)
    payment_currency = Column(String(3), default="USD")
    payment_method = Column(String(50))
    transaction_id = Column(String(100))
    coupon_used = Column(String(50))
    discount_amount = Column(Float, default=0.0)
    
    # Certificate
    certificate_issued = Column(Boolean, default=False)
    certificate_issued_at = Column(DateTime(timezone=True))
    certificate_url = Column(String(500))
    certificate_id = Column(String(100), unique=True)
    
    # Learning Path
    learning_path_id = Column(Integer, ForeignKey("learning_paths.id"))
    is_part_of_bundle = Column(Boolean, default=False)
    bundle_id = Column(Integer)
    
    # User Experience
    rating_given = Column(Float)
    review_submitted = Column(Boolean, default=False)
    favorite = Column(Boolean, default=False)
    notes = Column(JSON, default=list)  # User's personal notes
    
    # Relationships
    user = relationship("User", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")
    lesson_progress = relationship("LessonProgress", back_populates="enrollment", cascade="all, delete-orphan")
    quiz_attempts = relationship("QuizAttempt", back_populates="enrollment")
    assignments = relationship("AssignmentSubmission", back_populates="enrollment")
    
    def to_dict(self) -> Dict:
        """Convert enrollment to dictionary"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "course_id": self.course_id,
            "status": self.status,
            "enrolled_at": self.enrolled_at.isoformat() if self.enrolled_at else None,
            "progress_percentage": self.progress_percentage,
            "completed_lessons": self.completed_lessons,
            "total_time_spent": self.total_time_spent,
            "certificate_issued": self.certificate_issued,
            "last_accessed": self.last_accessed.isoformat() if self.last_accessed else None
        }

class LessonProgress(Base):
    __tablename__ = "lesson_progress"
    
    id = Column(Integer, primary_key=True, index=True)
    enrollment_id = Column(Integer, ForeignKey("enrollments.id"), nullable=False)
    lesson_id = Column(Integer, ForeignKey("lessons.id"), nullable=False)
    
    # Progress Details
    is_completed = Column(Boolean, default=False)
    completion_percentage = Column(Float, default=0.0)
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True))
    last_position = Column(Integer, default=0)  # For video lessons (in seconds)
    time_spent = Column(Integer, default=0)  # in minutes
    
    # Interaction Data
    play_count = Column(Integer, default=0)
    notes = Column(Text)
    bookmarks = Column(JSON, default=list)
    
    # Relationships
    enrollment = relationship("Enrollment", back_populates="lesson_progress")
    lesson = relationship("Lesson", back_populates="progress")

class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"
    
    id = Column(Integer, primary_key=True, index=True)
    enrollment_id = Column(Integer, ForeignKey("enrollments.id"), nullable=False)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"), nullable=False)
    
    # Attempt Details
    attempt_number = Column(Integer, default=1)
    score = Column(Float, nullable=False)
    max_score = Column(Float, nullable=False)
    percentage = Column(Float, nullable=False)
    passed = Column(Boolean, default=False)
    
    # Timing
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    submitted_at = Column(DateTime(timezone=True))
    time_taken = Column(Integer)  # in seconds
    
    # Answers
    answers = Column(JSON, nullable=False)  # Store user's answers
    feedback = Column(JSON)  # Store feedback for each question
    
    # Relationships
    enrollment = relationship("Enrollment", back_populates="quiz_attempts")
    quiz = relationship("Quiz", back_populates="attempts")

class AssignmentSubmission(Base):
    __tablename__ = "assignment_submissions"
    
    id = Column(Integer, primary_key=True, index=True)
    enrollment_id = Column(Integer, ForeignKey("enrollments.id"), nullable=False)
    assignment_id = Column(Integer, ForeignKey("assignments.id"), nullable=False)
    
    # Submission Details
    submission_text = Column(Text)
    submission_files = Column(JSON, default=list)  # List of file URLs
    submitted_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Grading
    is_graded = Column(Boolean, default=False)
    grade = Column(Float)
    max_grade = Column(Float)
    graded_at = Column(DateTime(timezone=True))
    graded_by = Column(Integer, ForeignKey("users.id"))
    
    # Feedback
    instructor_feedback = Column(Text)
    peer_reviews = Column(JSON, default=list)
    
    # Status
    status = Column(String(20), default="submitted")  # submitted, graded, returned, resubmitted
    resubmission_count = Column(Integer, default=0)
    
    # Relationships
    enrollment = relationship("Enrollment", back_populates="assignments")
    assignment = relationship("Assignment", back_populates="submissions")
    grader = relationship("User", foreign_keys=[graded_by])

class LearningPath(Base):
    __tablename__ = "learning_paths"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    
    # Path Details
    target_skill = Column(String(100))
    skill_level_start = Column(String(20))
    skill_level_target = Column(String(20))
    estimated_duration = Column(Integer)  # in days
    
    # Courses in Path
    course_sequence = Column(JSON, nullable=False)  # Ordered list of course IDs
    total_courses = Column(Integer, default=0)
    completed_courses = Column(Integer, default=0)
    
    # Progress
    progress_percentage = Column(Float, default=0.0)
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    target_completion = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    
    # AI Generated
    is_ai_generated = Column(Boolean, default=False)
    ai_recommendations = Column(JSON, default=dict)
    
    # Status
    is_active = Column(Boolean, default=True)
    is_public = Column(Boolean, default=False)  # Can be shared with others
    
    # Relationships
    user = relationship("User", back_populates="learning_paths")

class WatchHistory(Base):
    __tablename__ = "watch_history"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    lesson_id = Column(Integer, ForeignKey("lessons.id"))
    
    # Watch Details
    watched_at = Column(DateTime(timezone=True), server_default=func.now())
    duration = Column(Integer, default=0)  # in seconds
    completion_percentage = Column(Float, default=0.0)
    
    # Device & Session
    device_type = Column(String(50))
    browser = Column(String(50))
    ip_address = Column(String(45))
    session_id = Column(String(100))
    
    # Relationships
    user = relationship("User", back_populates="watch_history")
    course = relationship("Course")
    lesson = relationship("Lesson")

class Wishlist(Base):
    __tablename__ = "wishlists"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    added_at = Column(DateTime(timezone=True), server_default=func.now())
    priority = Column(Integer, default=0)
    notes = Column(Text)
    
    # Price tracking
    price_when_added = Column(Float)
    notify_on_discount = Column(Boolean, default=True)
    target_price = Column(Float)
    
    # Relationships
    user = relationship("User", back_populates="wishlist")
    course = relationship("Course")