"""Course model for the EUREKA marketplace"""
from sqlalchemy import Column, Integer, String, Float, Text, Boolean, DateTime, JSON, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
from typing import List, Dict, Optional
from enum import Enum

from config.database import Base

# Association tables for many-to-many relationships
course_tags = Table('course_tags',
    Base.metadata,
    Column('course_id', Integer, ForeignKey('courses.id')),
    Column('tag_id', Integer, ForeignKey('tags.id'))
)

course_prerequisites = Table('course_prerequisites',
    Base.metadata,
    Column('course_id', Integer, ForeignKey('courses.id')),
    Column('prerequisite_id', Integer, ForeignKey('courses.id'))
)

class CourseLevel(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"

class CourseStatus(str, Enum):
    DRAFT = "draft"
    UNDER_REVIEW = "under_review"
    PUBLISHED = "published"
    ARCHIVED = "archived"
    SUSPENDED = "suspended"

class Course(Base):
    __tablename__ = "courses"

    # Basic Information
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False, index=True)
    subtitle = Column(String(500))
    slug = Column(String(250), unique=True, index=True)
    description = Column(Text, nullable=False)
    short_description = Column(String(500))
    
    # Categorization
    category_id = Column(Integer, ForeignKey("categories.id"))
    subcategory_id = Column(Integer, ForeignKey("subcategories.id"))
    level = Column(String(20), default=CourseLevel.BEGINNER)
    language = Column(String(10), default="en")
    
    # Instructor Information
    instructor_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    co_instructors = Column(JSON, default=list)  # List of user IDs
    
    # Pricing
    price = Column(Float, default=0.0)
    original_price = Column(Float)
    discount_percentage = Column(Float, default=0.0)
    currency = Column(String(3), default="USD")
    is_free = Column(Boolean, default=False)
    
    # Course Content
    duration_hours = Column(Float, default=0.0)
    total_lectures = Column(Integer, default=0)
    total_quizzes = Column(Integer, default=0)
    total_assignments = Column(Integer, default=0)
    total_downloads = Column(Integer, default=0)
    
    # Learning Outcomes
    learning_objectives = Column(JSON, default=list)
    skills_gained = Column(JSON, default=list)
    requirements = Column(JSON, default=list)
    target_audience = Column(JSON, default=list)
    
    # Media
    thumbnail_url = Column(String(500))
    preview_video_url = Column(String(500))
    promotional_video_url = Column(String(500))
    
    # Statistics
    total_students = Column(Integer, default=0)
    average_rating = Column(Float, default=0.0)
    total_reviews = Column(Integer, default=0)
    completion_rate = Column(Float, default=0.0)
    
    # SEO & Marketing
    meta_title = Column(String(100))
    meta_description = Column(String(200))
    meta_keywords = Column(JSON, default=list)
    
    # Status & Timestamps
    status = Column(String(20), default=CourseStatus.DRAFT)
    is_featured = Column(Boolean, default=False)
    is_trending = Column(Boolean, default=False)
    is_bestseller = Column(Boolean, default=False)
    published_at = Column(DateTime(timezone=True))
    last_updated = Column(DateTime(timezone=True), onupdate=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Advanced Features
    certificate_enabled = Column(Boolean, default=True)
    certificate_template_id = Column(Integer)
    ai_generated_content = Column(JSON, default=dict)
    gamification_enabled = Column(Boolean, default=True)
    discussion_forum_enabled = Column(Boolean, default=True)
    
    # Relationships
    category = relationship("Category", back_populates="courses")
    subcategory = relationship("Subcategory", back_populates="courses")
    instructor = relationship("User", back_populates="taught_courses", foreign_keys=[instructor_id])
    modules = relationship("CourseModule", back_populates="course", cascade="all, delete-orphan")
    enrollments = relationship("Enrollment", back_populates="course")
    reviews = relationship("CourseReview", back_populates="course")
    tags = relationship("Tag", secondary=course_tags, back_populates="courses")
    prerequisites = relationship("Course", 
                                secondary=course_prerequisites,
                                primaryjoin=id==course_prerequisites.c.course_id,
                                secondaryjoin=id==course_prerequisites.c.prerequisite_id,
                                backref="required_for")
    announcements = relationship("CourseAnnouncement", back_populates="course")
    coupons = relationship("CourseCoupon", back_populates="course")
    
    def to_dict(self) -> Dict:
        """Convert course to dictionary"""
        return {
            "id": self.id,
            "title": self.title,
            "subtitle": self.subtitle,
            "slug": self.slug,
            "description": self.description,
            "level": self.level,
            "price": self.price,
            "original_price": self.original_price,
            "discount_percentage": self.discount_percentage,
            "duration_hours": self.duration_hours,
            "total_students": self.total_students,
            "average_rating": self.average_rating,
            "thumbnail_url": self.thumbnail_url,
            "instructor": {
                "id": self.instructor.id,
                "name": self.instructor.full_name,
                "avatar": self.instructor.avatar_url
            } if self.instructor else None,
            "is_featured": self.is_featured,
            "is_trending": self.is_trending,
            "is_bestseller": self.is_bestseller
        }

class CourseModule(Base):
    __tablename__ = "course_modules"
    
    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    order_index = Column(Integer, default=0)
    duration_minutes = Column(Integer, default=0)
    is_preview = Column(Boolean, default=False)
    
    # Relationships
    course = relationship("Course", back_populates="modules")
    lessons = relationship("Lesson", back_populates="module", cascade="all, delete-orphan")

class Lesson(Base):
    __tablename__ = "lessons"
    
    id = Column(Integer, primary_key=True, index=True)
    module_id = Column(Integer, ForeignKey("course_modules.id"), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    lesson_type = Column(String(20))  # video, article, quiz, assignment
    content_url = Column(String(500))
    duration_minutes = Column(Integer, default=0)
    order_index = Column(Integer, default=0)
    is_preview = Column(Boolean, default=False)
    is_downloadable = Column(Boolean, default=False)
    
    # Additional content
    transcript = Column(Text)
    resources = Column(JSON, default=list)
    
    # Relationships
    module = relationship("CourseModule", back_populates="lessons")
    progress = relationship("LessonProgress", back_populates="lesson")

class Category(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    slug = Column(String(100), unique=True, index=True)
    description = Column(Text)
    icon = Column(String(50))
    image_url = Column(String(500))
    parent_id = Column(Integer, ForeignKey("categories.id"))
    order_index = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    courses = relationship("Course", back_populates="category")
    subcategories = relationship("Subcategory", back_populates="category")

class Subcategory(Base):
    __tablename__ = "subcategories"
    
    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    name = Column(String(100), nullable=False)
    slug = Column(String(100), unique=True, index=True)
    description = Column(Text)
    order_index = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    category = relationship("Category", back_populates="subcategories")
    courses = relationship("Course", back_populates="subcategory")

class Tag(Base):
    __tablename__ = "tags"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    slug = Column(String(50), unique=True, index=True)
    usage_count = Column(Integer, default=0)
    
    # Relationships
    courses = relationship("Course", secondary=course_tags, back_populates="tags")

class CourseReview(Base):
    __tablename__ = "course_reviews"
    
    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    rating = Column(Float, nullable=False)
    title = Column(String(200))
    comment = Column(Text)
    is_verified_purchase = Column(Boolean, default=True)
    helpful_count = Column(Integer, default=0)
    reported_count = Column(Integer, default=0)
    instructor_response = Column(Text)
    responded_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    course = relationship("Course", back_populates="reviews")
    user = relationship("User", back_populates="course_reviews")

class CourseAnnouncement(Base):
    __tablename__ = "course_announcements"
    
    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    is_promotional = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    course = relationship("Course", back_populates="announcements")

class CourseCoupon(Base):
    __tablename__ = "course_coupons"
    
    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    code = Column(String(50), unique=True, nullable=False)
    discount_percentage = Column(Float)
    discount_amount = Column(Float)
    max_uses = Column(Integer)
    current_uses = Column(Integer, default=0)
    valid_from = Column(DateTime(timezone=True))
    valid_until = Column(DateTime(timezone=True))
    is_active = Column(Boolean, default=True)
    
    # Relationships
    course = relationship("Course", back_populates="coupons")