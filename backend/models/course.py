"""
Course Marketplace Database Models
Comprehensive models for the EUREKA Course Marketplace
"""

from sqlalchemy import Column, Integer, String, Float, Text, DateTime, Boolean, ForeignKey, JSON, Enum, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum

Base = declarative_base()

# Association tables for many-to-many relationships
course_tags = Table('course_tags', Base.metadata,
    Column('course_id', Integer, ForeignKey('courses.id')),
    Column('tag_id', Integer, ForeignKey('tags.id'))
)

course_categories = Table('course_categories', Base.metadata,
    Column('course_id', Integer, ForeignKey('courses.id')),
    Column('category_id', Integer, ForeignKey('categories.id'))
)

course_instructors = Table('course_instructors', Base.metadata,
    Column('course_id', Integer, ForeignKey('courses.id')),
    Column('instructor_id', Integer, ForeignKey('users.id'))
)

class CourseLevel(enum.Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    ALL_LEVELS = "all_levels"

class CourseStatus(enum.Enum):
    DRAFT = "draft"
    PENDING_REVIEW = "pending_review"
    PUBLISHED = "published"
    ARCHIVED = "archived"
    SUSPENDED = "suspended"

class Course(Base):
    __tablename__ = 'courses'
    
    # Basic Information
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False, index=True)
    subtitle = Column(String(300))
    slug = Column(String(200), unique=True, index=True)
    description = Column(Text)
    short_description = Column(String(500))
    
    # Categorization
    level = Column(Enum(CourseLevel), default=CourseLevel.ALL_LEVELS)
    language = Column(String(50), default="English")
    categories = relationship("Category", secondary=course_categories, back_populates="courses")
    tags = relationship("Tag", secondary=course_tags, back_populates="courses")
    
    # Pricing
    price = Column(Float, default=0.0)
    original_price = Column(Float)
    discount_percentage = Column(Float, default=0.0)
    currency = Column(String(10), default="USD")
    is_free = Column(Boolean, default=False)
    
    # Media
    thumbnail_url = Column(String(500))
    preview_video_url = Column(String(500))
    promotional_video_url = Column(String(500))
    
    # Content Details
    duration_hours = Column(Float)
    lecture_count = Column(Integer, default=0)
    article_count = Column(Integer, default=0)
    resource_count = Column(Integer, default=0)
    quiz_count = Column(Integer, default=0)
    assignment_count = Column(Integer, default=0)
    
    # Requirements & Outcomes
    requirements = Column(JSON)  # List of prerequisites
    learning_outcomes = Column(JSON)  # What students will learn
    target_audience = Column(JSON)  # Who this course is for
    
    # Instructor Information
    instructors = relationship("User", secondary=course_instructors, back_populates="courses_teaching")
    
    # Statistics
    rating = Column(Float, default=0.0)
    rating_count = Column(Integer, default=0)
    enrollment_count = Column(Integer, default=0)
    completion_rate = Column(Float, default=0.0)
    view_count = Column(Integer, default=0)
    
    # Features
    has_certificate = Column(Boolean, default=True)
    has_lifetime_access = Column(Boolean, default=True)
    has_money_back_guarantee = Column(Boolean, default=True)
    has_assignments = Column(Boolean, default=False)
    has_subtitles = Column(Boolean, default=False)
    subtitle_languages = Column(JSON)  # List of available subtitle languages
    
    # Status & Timestamps
    status = Column(Enum(CourseStatus), default=CourseStatus.DRAFT)
    published_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_updated_content = Column(DateTime)
    
    # SEO
    meta_title = Column(String(200))
    meta_description = Column(String(300))
    meta_keywords = Column(JSON)
    
    # Relationships
    modules = relationship("CourseModule", back_populates="course", cascade="all, delete-orphan")
    enrollments = relationship("Enrollment", back_populates="course")
    reviews = relationship("Review", back_populates="course")
    announcements = relationship("CourseAnnouncement", back_populates="course")
    questions = relationship("CourseQuestion", back_populates="course")
    
class CourseModule(Base):
    __tablename__ = 'course_modules'
    
    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey('courses.id'))
    title = Column(String(200), nullable=False)
    description = Column(Text)
    order = Column(Integer)
    duration_minutes = Column(Integer)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    course = relationship("Course", back_populates="modules")
    lessons = relationship("Lesson", back_populates="module", cascade="all, delete-orphan")

class LessonType(enum.Enum):
    VIDEO = "video"
    ARTICLE = "article"
    QUIZ = "quiz"
    ASSIGNMENT = "assignment"
    RESOURCE = "resource"
    LIVE_SESSION = "live_session"

class Lesson(Base):
    __tablename__ = 'lessons'
    
    id = Column(Integer, primary_key=True)
    module_id = Column(Integer, ForeignKey('course_modules.id'))
    title = Column(String(200), nullable=False)
    description = Column(Text)
    type = Column(Enum(LessonType), default=LessonType.VIDEO)
    order = Column(Integer)
    
    # Content
    video_url = Column(String(500))
    video_duration_seconds = Column(Integer)
    article_content = Column(Text)
    resource_urls = Column(JSON)
    
    # Settings
    is_preview = Column(Boolean, default=False)
    is_mandatory = Column(Boolean, default=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    module = relationship("CourseModule", back_populates="lessons")
    progress = relationship("LessonProgress", back_populates="lesson")
    
class Category(Base):
    __tablename__ = 'categories'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    slug = Column(String(100), unique=True)
    description = Column(Text)
    icon = Column(String(50))  # Font Awesome icon class
    parent_id = Column(Integer, ForeignKey('categories.id'))
    
    # Statistics
    course_count = Column(Integer, default=0)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    courses = relationship("Course", secondary=course_categories, back_populates="categories")
    subcategories = relationship("Category")

class Tag(Base):
    __tablename__ = 'tags'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    slug = Column(String(50), unique=True)
    usage_count = Column(Integer, default=0)
    
    # Relationships
    courses = relationship("Course", secondary=course_tags, back_populates="tags")

class Review(Base):
    __tablename__ = 'reviews'
    
    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey('courses.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    rating = Column(Float, nullable=False)
    title = Column(String(200))
    comment = Column(Text)
    
    # Helpful votes
    helpful_count = Column(Integer, default=0)
    not_helpful_count = Column(Integer, default=0)
    
    # Verification
    is_verified_purchase = Column(Boolean, default=True)
    instructor_response = Column(Text)
    instructor_response_date = Column(DateTime)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    course = relationship("Course", back_populates="reviews")
    user = relationship("User", back_populates="reviews")

class CourseAnnouncement(Base):
    __tablename__ = 'course_announcements'
    
    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey('courses.id'))
    instructor_id = Column(Integer, ForeignKey('users.id'))
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    is_promotional = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    course = relationship("Course", back_populates="announcements")
    instructor = relationship("User")

class CourseQuestion(Base):
    __tablename__ = 'course_questions'
    
    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey('courses.id'))
    lesson_id = Column(Integer, ForeignKey('lessons.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    title = Column(String(300), nullable=False)
    content = Column(Text, nullable=False)
    
    # Voting
    upvotes = Column(Integer, default=0)
    downvotes = Column(Integer, default=0)
    
    # Status
    is_answered = Column(Boolean, default=False)
    is_featured = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    course = relationship("Course", back_populates="questions")
    lesson = relationship("Lesson")
    user = relationship("User")
    answers = relationship("QuestionAnswer", back_populates="question")

class QuestionAnswer(Base):
    __tablename__ = 'question_answers'
    
    id = Column(Integer, primary_key=True)
    question_id = Column(Integer, ForeignKey('course_questions.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    content = Column(Text, nullable=False)
    
    # Voting
    upvotes = Column(Integer, default=0)
    downvotes = Column(Integer, default=0)
    
    # Status
    is_instructor_answer = Column(Boolean, default=False)
    is_accepted = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    question = relationship("CourseQuestion", back_populates="answers")
    user = relationship("User")