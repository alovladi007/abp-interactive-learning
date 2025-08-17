"""Course Marketplace API Routes for EUREKA Platform"""
from fastapi import APIRouter, HTTPException, Depends, Query, BackgroundTasks, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func, desc
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import logging

from models.course import Course, CourseModule, Lesson, Category, CourseReview, CourseStatus
from models.enrollment import Enrollment, LessonProgress, Wishlist, EnrollmentStatus
from services.recommendation import RecommendationService
from services.search import SearchService
from services.payment import PaymentService
from services.notification import NotificationService
from config.database import get_db
from utils.auth import get_current_user
from schemas.course import (
    CourseCreate, CourseUpdate, CourseResponse,
    CourseDetailResponse, CourseFilterParams,
    ModuleCreate, LessonCreate, ReviewCreate
)
from schemas.enrollment import EnrollmentCreate, EnrollmentResponse, ProgressUpdate

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/marketplace", tags=["marketplace"])

# Initialize services
recommendation_service = RecommendationService()
search_service = SearchService()
payment_service = PaymentService()
notification_service = NotificationService()

# ==================== Course Discovery ====================

@router.get("/courses", response_model=List[CourseResponse])
async def get_courses(
    category: Optional[str] = None,
    level: Optional[str] = None,
    price_min: Optional[float] = None,
    price_max: Optional[float] = None,
    rating_min: Optional[float] = None,
    duration_min: Optional[float] = None,
    duration_max: Optional[float] = None,
    language: Optional[str] = "en",
    sort_by: str = "popularity",
    search: Optional[str] = None,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get courses with advanced filtering and sorting"""
    try:
        query = db.query(Course).filter(Course.status == CourseStatus.PUBLISHED)
        
        # Apply filters
        if category:
            query = query.join(Category).filter(Category.slug == category)
        if level:
            query = query.filter(Course.level == level)
        if price_min is not None:
            query = query.filter(Course.price >= price_min)
        if price_max is not None:
            query = query.filter(Course.price <= price_max)
        if rating_min:
            query = query.filter(Course.average_rating >= rating_min)
        if duration_min:
            query = query.filter(Course.duration_hours >= duration_min)
        if duration_max:
            query = query.filter(Course.duration_hours <= duration_max)
        if language:
            query = query.filter(Course.language == language)
        
        # Search
        if search:
            search_results = await search_service.search_courses(search, db)
            course_ids = [r["id"] for r in search_results]
            query = query.filter(Course.id.in_(course_ids))
        
        # Sorting
        if sort_by == "popularity":
            query = query.order_by(desc(Course.total_students))
        elif sort_by == "rating":
            query = query.order_by(desc(Course.average_rating))
        elif sort_by == "newest":
            query = query.order_by(desc(Course.created_at))
        elif sort_by == "price_low":
            query = query.order_by(Course.price)
        elif sort_by == "price_high":
            query = query.order_by(desc(Course.price))
        
        # Pagination
        offset = (page - 1) * limit
        courses = query.offset(offset).limit(limit).all()
        
        return [CourseResponse.from_orm(course) for course in courses]
    
    except Exception as e:
        logger.error(f"Error fetching courses: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch courses")

@router.get("/courses/trending", response_model=List[CourseResponse])
async def get_trending_courses(
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """Get trending courses based on recent enrollments and engagement"""
    try:
        # Calculate trending score based on recent enrollments and views
        week_ago = datetime.utcnow() - timedelta(days=7)
        
        trending = db.query(
            Course,
            func.count(Enrollment.id).label('recent_enrollments')
        ).join(
            Enrollment, Course.id == Enrollment.course_id
        ).filter(
            Enrollment.enrolled_at >= week_ago,
            Course.status == CourseStatus.PUBLISHED
        ).group_by(Course.id).order_by(
            desc('recent_enrollments')
        ).limit(limit).all()
        
        return [CourseResponse.from_orm(course) for course, _ in trending]
    
    except Exception as e:
        logger.error(f"Error fetching trending courses: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch trending courses")

@router.get("/courses/recommended", response_model=List[CourseResponse])
async def get_recommended_courses(
    limit: int = Query(10, ge=1, le=50),
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get personalized course recommendations for the current user"""
    try:
        recommendations = await recommendation_service.get_recommendations(
            user_id=current_user.id,
            limit=limit,
            db=db
        )
        
        return recommendations
    
    except Exception as e:
        logger.error(f"Error getting recommendations: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get recommendations")

@router.get("/courses/{course_id}", response_model=CourseDetailResponse)
async def get_course_details(
    course_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get detailed information about a specific course"""
    try:
        course = db.query(Course).filter(Course.id == course_id).first()
        
        if not course:
            raise HTTPException(status_code=404, detail="Course not found")
        
        # Check if user is enrolled
        enrollment = db.query(Enrollment).filter(
            Enrollment.user_id == current_user.id,
            Enrollment.course_id == course_id
        ).first()
        
        # Get course modules and lessons
        modules = db.query(CourseModule).filter(
            CourseModule.course_id == course_id
        ).order_by(CourseModule.order_index).all()
        
        # Get reviews
        reviews = db.query(CourseReview).filter(
            CourseReview.course_id == course_id
        ).order_by(desc(CourseReview.helpful_count)).limit(10).all()
        
        # Track view for recommendations
        await recommendation_service.track_view(current_user.id, course_id, db)
        
        response = CourseDetailResponse.from_orm(course)
        response.is_enrolled = enrollment is not None
        response.modules = modules
        response.reviews = reviews
        
        return response
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching course details: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch course details")

# ==================== Course Management (Instructor) ====================

@router.post("/courses", response_model=CourseResponse)
async def create_course(
    course_data: CourseCreate,
    background_tasks: BackgroundTasks,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new course (instructor only)"""
    try:
        # Check if user is an instructor
        if not current_user.is_instructor:
            raise HTTPException(status_code=403, detail="Only instructors can create courses")
        
        # Create course
        course = Course(
            **course_data.dict(),
            instructor_id=current_user.id,
            status=CourseStatus.DRAFT
        )
        
        db.add(course)
        db.commit()
        db.refresh(course)
        
        # Send notification
        background_tasks.add_task(
            notification_service.notify_course_created,
            course.id,
            current_user.id
        )
        
        return CourseResponse.from_orm(course)
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating course: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to create course")

@router.put("/courses/{course_id}", response_model=CourseResponse)
async def update_course(
    course_id: int,
    course_data: CourseUpdate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update course details (instructor only)"""
    try:
        course = db.query(Course).filter(Course.id == course_id).first()
        
        if not course:
            raise HTTPException(status_code=404, detail="Course not found")
        
        if course.instructor_id != current_user.id:
            raise HTTPException(status_code=403, detail="You can only edit your own courses")
        
        # Update course
        for key, value in course_data.dict(exclude_unset=True).items():
            setattr(course, key, value)
        
        course.last_updated = datetime.utcnow()
        db.commit()
        db.refresh(course)
        
        return CourseResponse.from_orm(course)
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating course: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to update course")

@router.post("/courses/{course_id}/modules", response_model=Dict[str, Any])
async def add_course_module(
    course_id: int,
    module_data: ModuleCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Add a module to a course"""
    try:
        course = db.query(Course).filter(Course.id == course_id).first()
        
        if not course:
            raise HTTPException(status_code=404, detail="Course not found")
        
        if course.instructor_id != current_user.id:
            raise HTTPException(status_code=403, detail="You can only edit your own courses")
        
        # Create module
        module = CourseModule(
            course_id=course_id,
            **module_data.dict()
        )
        
        db.add(module)
        db.commit()
        db.refresh(module)
        
        return {"message": "Module added successfully", "module_id": module.id}
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error adding module: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to add module")

@router.post("/courses/{course_id}/publish")
async def publish_course(
    course_id: int,
    background_tasks: BackgroundTasks,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Publish a course for public access"""
    try:
        course = db.query(Course).filter(Course.id == course_id).first()
        
        if not course:
            raise HTTPException(status_code=404, detail="Course not found")
        
        if course.instructor_id != current_user.id:
            raise HTTPException(status_code=403, detail="You can only publish your own courses")
        
        # Validate course is ready for publishing
        if not course.modules or len(course.modules) == 0:
            raise HTTPException(status_code=400, detail="Course must have at least one module")
        
        # Update status
        course.status = CourseStatus.UNDER_REVIEW
        course.published_at = datetime.utcnow()
        db.commit()
        
        # Trigger review process
        background_tasks.add_task(
            notification_service.notify_course_under_review,
            course.id
        )
        
        return {"message": "Course submitted for review", "status": course.status}
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error publishing course: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to publish course")

# ==================== Enrollment & Progress ====================

@router.post("/courses/{course_id}/enroll", response_model=EnrollmentResponse)
async def enroll_in_course(
    course_id: int,
    payment_method: Optional[str] = None,
    coupon_code: Optional[str] = None,
    background_tasks: BackgroundTasks = None,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Enroll in a course"""
    try:
        # Check if course exists
        course = db.query(Course).filter(Course.id == course_id).first()
        if not course:
            raise HTTPException(status_code=404, detail="Course not found")
        
        # Check if already enrolled
        existing = db.query(Enrollment).filter(
            Enrollment.user_id == current_user.id,
            Enrollment.course_id == course_id
        ).first()
        
        if existing:
            raise HTTPException(status_code=400, detail="Already enrolled in this course")
        
        # Process payment if not free
        payment_status = "completed"
        payment_amount = course.price
        discount_amount = 0.0
        
        if not course.is_free and course.price > 0:
            # Apply coupon if provided
            if coupon_code:
                discount = await payment_service.validate_coupon(coupon_code, course_id, db)
                discount_amount = discount.get("discount_amount", 0)
                payment_amount -= discount_amount
            
            # Process payment
            payment_result = await payment_service.process_payment(
                user_id=current_user.id,
                amount=payment_amount,
                payment_method=payment_method,
                course_id=course_id
            )
            
            if not payment_result["success"]:
                raise HTTPException(status_code=400, detail="Payment failed")
        
        # Create enrollment
        enrollment = Enrollment(
            user_id=current_user.id,
            course_id=course_id,
            status=EnrollmentStatus.ACTIVE,
            payment_status=payment_status,
            payment_amount=payment_amount,
            payment_method=payment_method,
            coupon_used=coupon_code,
            discount_amount=discount_amount
        )
        
        db.add(enrollment)
        
        # Update course statistics
        course.total_students += 1
        
        db.commit()
        db.refresh(enrollment)
        
        # Send notifications
        background_tasks.add_task(
            notification_service.notify_enrollment,
            enrollment.id
        )
        
        return EnrollmentResponse.from_orm(enrollment)
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error enrolling in course: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to enroll in course")

@router.get("/enrollments", response_model=List[EnrollmentResponse])
async def get_user_enrollments(
    status: Optional[str] = None,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's enrolled courses"""
    try:
        query = db.query(Enrollment).filter(Enrollment.user_id == current_user.id)
        
        if status:
            query = query.filter(Enrollment.status == status)
        
        enrollments = query.order_by(desc(Enrollment.enrolled_at)).all()
        
        return [EnrollmentResponse.from_orm(e) for e in enrollments]
    
    except Exception as e:
        logger.error(f"Error fetching enrollments: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch enrollments")

@router.post("/courses/{course_id}/progress", response_model=Dict[str, Any])
async def update_lesson_progress(
    course_id: int,
    lesson_id: int,
    progress_data: ProgressUpdate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update lesson progress"""
    try:
        # Get enrollment
        enrollment = db.query(Enrollment).filter(
            Enrollment.user_id == current_user.id,
            Enrollment.course_id == course_id
        ).first()
        
        if not enrollment:
            raise HTTPException(status_code=404, detail="Enrollment not found")
        
        # Get or create lesson progress
        progress = db.query(LessonProgress).filter(
            LessonProgress.enrollment_id == enrollment.id,
            LessonProgress.lesson_id == lesson_id
        ).first()
        
        if not progress:
            progress = LessonProgress(
                enrollment_id=enrollment.id,
                lesson_id=lesson_id
            )
            db.add(progress)
        
        # Update progress
        progress.completion_percentage = progress_data.completion_percentage
        progress.last_position = progress_data.last_position
        progress.time_spent += progress_data.time_spent
        
        if progress_data.completion_percentage >= 100:
            progress.is_completed = True
            progress.completed_at = datetime.utcnow()
            enrollment.completed_lessons += 1
        
        # Update enrollment progress
        enrollment.last_accessed = datetime.utcnow()
        enrollment.total_time_spent += progress_data.time_spent
        
        # Calculate overall progress
        total_lessons = db.query(Lesson).join(CourseModule).filter(
            CourseModule.course_id == course_id
        ).count()
        
        if total_lessons > 0:
            enrollment.progress_percentage = (enrollment.completed_lessons / total_lessons) * 100
        
        db.commit()
        
        return {
            "lesson_progress": progress.completion_percentage,
            "course_progress": enrollment.progress_percentage,
            "completed_lessons": enrollment.completed_lessons,
            "total_lessons": total_lessons
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating progress: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to update progress")

# ==================== Reviews & Ratings ====================

@router.post("/courses/{course_id}/reviews", response_model=Dict[str, Any])
async def add_course_review(
    course_id: int,
    review_data: ReviewCreate,
    background_tasks: BackgroundTasks,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Add a review for a course"""
    try:
        # Check enrollment
        enrollment = db.query(Enrollment).filter(
            Enrollment.user_id == current_user.id,
            Enrollment.course_id == course_id
        ).first()
        
        if not enrollment:
            raise HTTPException(status_code=403, detail="You must be enrolled to review this course")
        
        # Check if already reviewed
        existing = db.query(CourseReview).filter(
            CourseReview.user_id == current_user.id,
            CourseReview.course_id == course_id
        ).first()
        
        if existing:
            raise HTTPException(status_code=400, detail="You have already reviewed this course")
        
        # Create review
        review = CourseReview(
            course_id=course_id,
            user_id=current_user.id,
            **review_data.dict()
        )
        
        db.add(review)
        
        # Update course rating
        course = db.query(Course).filter(Course.id == course_id).first()
        reviews = db.query(CourseReview).filter(CourseReview.course_id == course_id).all()
        
        total_rating = sum(r.rating for r in reviews) + review.rating
        course.average_rating = total_rating / (len(reviews) + 1)
        course.total_reviews = len(reviews) + 1
        
        # Update enrollment
        enrollment.rating_given = review.rating
        enrollment.review_submitted = True
        
        db.commit()
        
        # Notify instructor
        background_tasks.add_task(
            notification_service.notify_new_review,
            review.id
        )
        
        return {"message": "Review added successfully", "review_id": review.id}
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error adding review: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to add review")

@router.get("/courses/{course_id}/reviews", response_model=List[Dict[str, Any]])
async def get_course_reviews(
    course_id: int,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    sort_by: str = "helpful",
    db: Session = Depends(get_db)
):
    """Get reviews for a course"""
    try:
        query = db.query(CourseReview).filter(CourseReview.course_id == course_id)
        
        # Sorting
        if sort_by == "helpful":
            query = query.order_by(desc(CourseReview.helpful_count))
        elif sort_by == "newest":
            query = query.order_by(desc(CourseReview.created_at))
        elif sort_by == "rating_high":
            query = query.order_by(desc(CourseReview.rating))
        elif sort_by == "rating_low":
            query = query.order_by(CourseReview.rating)
        
        # Pagination
        offset = (page - 1) * limit
        reviews = query.offset(offset).limit(limit).all()
        
        return [
            {
                "id": r.id,
                "rating": r.rating,
                "title": r.title,
                "comment": r.comment,
                "helpful_count": r.helpful_count,
                "created_at": r.created_at.isoformat(),
                "user": {
                    "id": r.user.id,
                    "name": r.user.full_name,
                    "avatar": r.user.avatar_url
                },
                "instructor_response": r.instructor_response,
                "responded_at": r.responded_at.isoformat() if r.responded_at else None
            }
            for r in reviews
        ]
    
    except Exception as e:
        logger.error(f"Error fetching reviews: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch reviews")

# ==================== Wishlist ====================

@router.post("/wishlist/{course_id}")
async def add_to_wishlist(
    course_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Add a course to wishlist"""
    try:
        # Check if course exists
        course = db.query(Course).filter(Course.id == course_id).first()
        if not course:
            raise HTTPException(status_code=404, detail="Course not found")
        
        # Check if already in wishlist
        existing = db.query(Wishlist).filter(
            Wishlist.user_id == current_user.id,
            Wishlist.course_id == course_id
        ).first()
        
        if existing:
            raise HTTPException(status_code=400, detail="Course already in wishlist")
        
        # Add to wishlist
        wishlist = Wishlist(
            user_id=current_user.id,
            course_id=course_id,
            price_when_added=course.price
        )
        
        db.add(wishlist)
        db.commit()
        
        return {"message": "Added to wishlist"}
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error adding to wishlist: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to add to wishlist")

@router.delete("/wishlist/{course_id}")
async def remove_from_wishlist(
    course_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Remove a course from wishlist"""
    try:
        wishlist = db.query(Wishlist).filter(
            Wishlist.user_id == current_user.id,
            Wishlist.course_id == course_id
        ).first()
        
        if not wishlist:
            raise HTTPException(status_code=404, detail="Course not in wishlist")
        
        db.delete(wishlist)
        db.commit()
        
        return {"message": "Removed from wishlist"}
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error removing from wishlist: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to remove from wishlist")

@router.get("/wishlist", response_model=List[CourseResponse])
async def get_wishlist(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's wishlist"""
    try:
        wishlist = db.query(Wishlist).filter(
            Wishlist.user_id == current_user.id
        ).order_by(desc(Wishlist.added_at)).all()
        
        courses = [w.course for w in wishlist]
        
        return [CourseResponse.from_orm(c) for c in courses]
    
    except Exception as e:
        logger.error(f"Error fetching wishlist: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch wishlist")

# ==================== Categories ====================

@router.get("/categories", response_model=List[Dict[str, Any]])
async def get_categories(db: Session = Depends(get_db)):
    """Get all course categories"""
    try:
        categories = db.query(Category).filter(
            Category.is_active == True
        ).order_by(Category.order_index).all()
        
        return [
            {
                "id": c.id,
                "name": c.name,
                "slug": c.slug,
                "description": c.description,
                "icon": c.icon,
                "image_url": c.image_url,
                "course_count": len(c.courses),
                "subcategories": [
                    {
                        "id": s.id,
                        "name": s.name,
                        "slug": s.slug,
                        "course_count": len(s.courses)
                    }
                    for s in c.subcategories
                ]
            }
            for c in categories
        ]
    
    except Exception as e:
        logger.error(f"Error fetching categories: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch categories")