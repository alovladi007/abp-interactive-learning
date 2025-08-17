"""
User and Enrollment Models for EUREKA Platform
"""

from sqlalchemy import Column, Integer, String, Float, Text, DateTime, Boolean, ForeignKey, JSON, Enum, Table
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from .course import Base, course_instructors

class UserRole(enum.Enum):
    STUDENT = "student"
    INSTRUCTOR = "instructor"
    ADMIN = "admin"
    MODERATOR = "moderator"

class UserStatus(enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    DELETED = "deleted"

class User(Base):
    __tablename__ = 'users'
    
    # Basic Information
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    
    # Profile Information
    first_name = Column(String(100))
    last_name = Column(String(100))
    display_name = Column(String(200))
    bio = Column(Text)
    headline = Column(String(200))
    
    # Contact & Location
    phone = Column(String(20))
    country = Column(String(100))
    city = Column(String(100))
    timezone = Column(String(50))
    language = Column(String(20), default="en")
    
    # Avatar & Media
    avatar_url = Column(String(500))
    cover_image_url = Column(String(500))
    
    # Role & Permissions
    role = Column(Enum(UserRole), default=UserRole.STUDENT)
    is_verified = Column(Boolean, default=False)
    is_pro_member = Column(Boolean, default=False)
    
    # Instructor Specific
    instructor_rating = Column(Float, default=0.0)
    instructor_rating_count = Column(Integer, default=0)
    instructor_bio = Column(Text)
    instructor_specialties = Column(JSON)  # List of specialties
    instructor_achievements = Column(JSON)  # List of achievements
    total_students = Column(Integer, default=0)
    total_reviews = Column(Integer, default=0)
    
    # Social Links
    website_url = Column(String(500))
    linkedin_url = Column(String(500))
    twitter_url = Column(String(500))
    youtube_url = Column(String(500))
    
    # Settings & Preferences
    email_notifications = Column(Boolean, default=True)
    push_notifications = Column(Boolean, default=True)
    marketing_emails = Column(Boolean, default=True)
    preferences = Column(JSON)  # User preferences dictionary
    
    # Security
    two_factor_enabled = Column(Boolean, default=False)
    two_factor_secret = Column(String(255))
    last_login = Column(DateTime)
    last_ip_address = Column(String(50))
    failed_login_attempts = Column(Integer, default=0)
    
    # Status & Timestamps
    status = Column(Enum(UserStatus), default=UserStatus.ACTIVE)
    email_verified_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    enrollments = relationship("Enrollment", back_populates="user")
    courses_teaching = relationship("Course", secondary=course_instructors, back_populates="instructors")
    reviews = relationship("Review", back_populates="user")
    certificates = relationship("Certificate", back_populates="user")
    wishlist = relationship("Wishlist", back_populates="user")
    cart_items = relationship("CartItem", back_populates="user")
    transactions = relationship("Transaction", back_populates="user")
    notifications = relationship("Notification", back_populates="user")
    learning_paths = relationship("UserLearningPath", back_populates="user")

class EnrollmentStatus(enum.Enum):
    ACTIVE = "active"
    COMPLETED = "completed"
    EXPIRED = "expired"
    SUSPENDED = "suspended"

class Enrollment(Base):
    __tablename__ = 'enrollments'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    course_id = Column(Integer, ForeignKey('courses.id'))
    
    # Progress Tracking
    progress_percentage = Column(Float, default=0.0)
    completed_lessons = Column(Integer, default=0)
    total_lessons = Column(Integer, default=0)
    last_accessed_lesson_id = Column(Integer, ForeignKey('lessons.id'))
    
    # Time Tracking
    total_watch_time_seconds = Column(Integer, default=0)
    last_accessed_at = Column(DateTime)
    
    # Status
    status = Column(Enum(EnrollmentStatus), default=EnrollmentStatus.ACTIVE)
    completed_at = Column(DateTime)
    certificate_issued = Column(Boolean, default=False)
    
    # Purchase Information
    purchase_price = Column(Float)
    purchase_currency = Column(String(10))
    transaction_id = Column(Integer, ForeignKey('transactions.id'))
    
    # Timestamps
    enrolled_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)  # For time-limited access
    
    # Relationships
    user = relationship("User", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")
    lesson_progress = relationship("LessonProgress", back_populates="enrollment")
    quiz_attempts = relationship("QuizAttempt", back_populates="enrollment")
    assignments = relationship("AssignmentSubmission", back_populates="enrollment")

class LessonProgress(Base):
    __tablename__ = 'lesson_progress'
    
    id = Column(Integer, primary_key=True)
    enrollment_id = Column(Integer, ForeignKey('enrollments.id'))
    lesson_id = Column(Integer, ForeignKey('lessons.id'))
    
    # Progress
    is_completed = Column(Boolean, default=False)
    progress_percentage = Column(Float, default=0.0)
    
    # Video Progress
    video_watch_time_seconds = Column(Integer, default=0)
    video_last_position_seconds = Column(Integer, default=0)
    
    # Timestamps
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)
    last_accessed_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    enrollment = relationship("Enrollment", back_populates="lesson_progress")
    lesson = relationship("Lesson", back_populates="progress")

class Certificate(Base):
    __tablename__ = 'certificates'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    course_id = Column(Integer, ForeignKey('courses.id'))
    enrollment_id = Column(Integer, ForeignKey('enrollments.id'))
    
    # Certificate Details
    certificate_number = Column(String(100), unique=True)
    certificate_url = Column(String(500))
    
    # Verification
    verification_code = Column(String(100), unique=True)
    is_valid = Column(Boolean, default=True)
    
    # Timestamps
    issued_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)  # If certificate has expiry
    
    # Relationships
    user = relationship("User", back_populates="certificates")

class Wishlist(Base):
    __tablename__ = 'wishlists'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    course_id = Column(Integer, ForeignKey('courses.id'))
    
    added_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="wishlist")

class CartItem(Base):
    __tablename__ = 'cart_items'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    course_id = Column(Integer, ForeignKey('courses.id'))
    
    # Pricing at time of addition
    price = Column(Float)
    discount_percentage = Column(Float)
    coupon_code = Column(String(50))
    
    added_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="cart_items")

class QuizAttempt(Base):
    __tablename__ = 'quiz_attempts'
    
    id = Column(Integer, primary_key=True)
    enrollment_id = Column(Integer, ForeignKey('enrollments.id'))
    quiz_id = Column(Integer, ForeignKey('lessons.id'))
    
    # Scoring
    score = Column(Float)
    max_score = Column(Float)
    percentage = Column(Float)
    
    # Details
    answers = Column(JSON)  # Store user's answers
    is_passed = Column(Boolean)
    time_taken_seconds = Column(Integer)
    
    # Timestamps
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)
    
    # Relationships
    enrollment = relationship("Enrollment", back_populates="quiz_attempts")

class AssignmentSubmission(Base):
    __tablename__ = 'assignment_submissions'
    
    id = Column(Integer, primary_key=True)
    enrollment_id = Column(Integer, ForeignKey('enrollments.id'))
    assignment_id = Column(Integer, ForeignKey('lessons.id'))
    
    # Submission
    submission_text = Column(Text)
    submission_files = Column(JSON)  # List of file URLs
    
    # Grading
    grade = Column(Float)
    max_grade = Column(Float)
    feedback = Column(Text)
    graded_by = Column(Integer, ForeignKey('users.id'))
    
    # Status
    is_submitted = Column(Boolean, default=False)
    is_graded = Column(Boolean, default=False)
    is_late = Column(Boolean, default=False)
    
    # Timestamps
    submitted_at = Column(DateTime)
    graded_at = Column(DateTime)
    
    # Relationships
    enrollment = relationship("Enrollment", back_populates="assignments")

class UserLearningPath(Base):
    __tablename__ = 'user_learning_paths'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    learning_path_id = Column(Integer, ForeignKey('learning_paths.id'))
    
    # Progress
    progress_percentage = Column(Float, default=0.0)
    completed_courses = Column(Integer, default=0)
    total_courses = Column(Integer)
    
    # Status
    is_active = Column(Boolean, default=True)
    is_completed = Column(Boolean, default=False)
    
    # Timestamps
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)
    target_completion_date = Column(DateTime)
    
    # Relationships
    user = relationship("User", back_populates="learning_paths")

class LearningPath(Base):
    __tablename__ = 'learning_paths'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    slug = Column(String(200), unique=True)
    
    # Details
    difficulty_level = Column(String(50))
    estimated_hours = Column(Integer)
    course_ids = Column(JSON)  # Ordered list of course IDs
    
    # Statistics
    enrollment_count = Column(Integer, default=0)
    completion_rate = Column(Float, default=0.0)
    rating = Column(Float, default=0.0)
    
    # Media
    thumbnail_url = Column(String(500))
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)