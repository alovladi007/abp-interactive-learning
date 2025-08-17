"""
Course Marketplace API Endpoints
Comprehensive REST API for EUREKA Course Marketplace
"""

from fastapi import APIRouter, Depends, HTTPException, Query, File, UploadFile, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import json

from ..database import get_db
from ..models.course import Course, CourseModule, Lesson, Category, Tag, Review, CourseQuestion
from ..models.user import User, Enrollment, LessonProgress, Certificate, Wishlist, CartItem
from ..models.payment import Transaction, Coupon, Notification
from ..auth import get_current_user, require_instructor, require_admin
from ..schemas import course_schemas as schemas
from ..services.recommendation import RecommendationService
from ..services.payment import PaymentService
from ..services.email import EmailService
from ..utils import generate_slug, upload_file_to_s3

router = APIRouter(prefix="/api/marketplace", tags=["marketplace"])

# ==================== Course Discovery ====================

@router.get("/courses", response_model=schemas.CourseListResponse)
async def get_courses(
    category: Optional[str] = None,
    level: Optional[str] = None,
    language: Optional[str] = Query("English"),
    min_price: Optional[float] = 0,
    max_price: Optional[float] = 10000,
    min_rating: Optional[float] = 0,
    search: Optional[str] = None,
    sort_by: str = Query("popularity", regex="^(popularity|rating|newest|price_low|price_high)$"),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Get courses with advanced filtering, searching, and sorting
    """
    query = db.query(Course).filter(Course.status == "published")
    
    # Apply filters
    if category:
        query = query.join(Course.categories).filter(Category.slug == category)
    
    if level:
        query = query.filter(Course.level == level)
    
    if language:
        query = query.filter(Course.language == language)
    
    query = query.filter(
        Course.price >= min_price,
        Course.price <= max_price,
        Course.rating >= min_rating
    )
    
    # Search
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            (Course.title.ilike(search_term)) |
            (Course.description.ilike(search_term)) |
            (Course.tags.any(Tag.name.ilike(search_term)))
        )
    
    # Sorting
    if sort_by == "popularity":
        query = query.order_by(Course.enrollment_count.desc())
    elif sort_by == "rating":
        query = query.order_by(Course.rating.desc())
    elif sort_by == "newest":
        query = query.order_by(Course.created_at.desc())
    elif sort_by == "price_low":
        query = query.order_by(Course.price.asc())
    elif sort_by == "price_high":
        query = query.order_by(Course.price.desc())
    
    # Pagination
    total = query.count()
    courses = query.offset((page - 1) * limit).limit(limit).all()
    
    return {
        "courses": courses,
        "total": total,
        "page": page,
        "pages": (total + limit - 1) // limit
    }

@router.get("/courses/trending", response_model=List[schemas.CourseCard])
async def get_trending_courses(
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """
    Get trending courses based on recent enrollments and views
    """
    # Calculate trending score based on recent activity
    week_ago = datetime.utcnow() - timedelta(days=7)
    
    courses = db.query(Course)\
        .filter(Course.status == "published")\
        .join(Enrollment)\
        .filter(Enrollment.enrolled_at >= week_ago)\
        .group_by(Course.id)\
        .order_by(db.func.count(Enrollment.id).desc())\
        .limit(limit)\
        .all()
    
    return courses

@router.get("/courses/recommended", response_model=List[schemas.CourseRecommendation])
async def get_recommended_courses(
    current_user: User = Depends(get_current_user),
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """
    Get personalized course recommendations using AI/ML
    """
    recommendation_service = RecommendationService(db)
    recommendations = recommendation_service.get_recommendations(
        user_id=current_user.id,
        limit=limit
    )
    
    return recommendations

@router.get("/courses/{course_id}", response_model=schemas.CourseDetail)
async def get_course_detail(
    course_id: int,
    current_user: Optional[User] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get detailed course information including curriculum
    """
    course = db.query(Course).filter(Course.id == course_id).first()
    
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    # Track view
    course.view_count += 1
    db.commit()
    
    # Check if user is enrolled
    is_enrolled = False
    if current_user:
        enrollment = db.query(Enrollment).filter(
            Enrollment.user_id == current_user.id,
            Enrollment.course_id == course_id
        ).first()
        is_enrolled = enrollment is not None
    
    return {
        **course.__dict__,
        "is_enrolled": is_enrolled,
        "modules": course.modules,
        "instructors": course.instructors,
        "reviews": course.reviews[:5]  # Top 5 reviews
    }

# ==================== Course Management (Instructors) ====================

@router.post("/courses", response_model=schemas.Course)
async def create_course(
    course_data: schemas.CourseCreate,
    current_user: User = Depends(require_instructor),
    db: Session = Depends(get_db)
):
    """
    Create a new course (instructors only)
    """
    course = Course(
        **course_data.dict(),
        slug=generate_slug(course_data.title)
    )
    
    # Add instructor
    course.instructors.append(current_user)
    
    db.add(course)
    db.commit()
    db.refresh(course)
    
    # Send notification
    notification = Notification(
        user_id=current_user.id,
        type="course_update",
        title="Course Created Successfully",
        message=f"Your course '{course.title}' has been created and is now in draft status.",
        action_url=f"/instructor/courses/{course.id}"
    )
    db.add(notification)
    db.commit()
    
    return course

@router.put("/courses/{course_id}", response_model=schemas.Course)
async def update_course(
    course_id: int,
    course_data: schemas.CourseUpdate,
    current_user: User = Depends(require_instructor),
    db: Session = Depends(get_db)
):
    """
    Update course details (instructors only)
    """
    course = db.query(Course).filter(Course.id == course_id).first()
    
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    # Check if user is instructor of this course
    if current_user not in course.instructors:
        raise HTTPException(status_code=403, detail="Not authorized to update this course")
    
    for key, value in course_data.dict(exclude_unset=True).items():
        setattr(course, key, value)
    
    course.updated_at = datetime.utcnow()
    course.last_updated_content = datetime.utcnow()
    
    db.commit()
    db.refresh(course)
    
    return course

@router.post("/courses/{course_id}/modules", response_model=schemas.CourseModule)
async def add_course_module(
    course_id: int,
    module_data: schemas.ModuleCreate,
    current_user: User = Depends(require_instructor),
    db: Session = Depends(get_db)
):
    """
    Add a module to the course curriculum
    """
    course = db.query(Course).filter(Course.id == course_id).first()
    
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    if current_user not in course.instructors:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    module = CourseModule(
        course_id=course_id,
        **module_data.dict()
    )
    
    db.add(module)
    db.commit()
    db.refresh(module)
    
    # Update course statistics
    course.lecture_count = sum(1 for m in course.modules for l in m.lessons if l.type == "video")
    course.duration_hours = sum(m.duration_minutes for m in course.modules) / 60
    db.commit()
    
    return module

@router.post("/courses/{course_id}/publish")
async def publish_course(
    course_id: int,
    current_user: User = Depends(require_instructor),
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Submit course for review and publication
    """
    course = db.query(Course).filter(Course.id == course_id).first()
    
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    if current_user not in course.instructors:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Validate course completeness
    if not course.modules or len(course.modules) < 3:
        raise HTTPException(status_code=400, detail="Course must have at least 3 modules")
    
    course.status = "pending_review"
    course.published_at = datetime.utcnow()
    db.commit()
    
    # Send for review (background task)
    background_tasks.add_task(review_course_quality, course_id)
    
    return {"message": "Course submitted for review"}

# ==================== Enrollment & Progress ====================

@router.post("/courses/{course_id}/enroll")
async def enroll_in_course(
    course_id: int,
    payment_method: Optional[str] = None,
    coupon_code: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Enroll in a course (handles payment if required)
    """
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
    
    # Handle payment if not free
    if not course.is_free and course.price > 0:
        payment_service = PaymentService(db)
        transaction = payment_service.process_payment(
            user=current_user,
            course=course,
            payment_method=payment_method,
            coupon_code=coupon_code
        )
        
        if transaction.status != "completed":
            raise HTTPException(status_code=402, detail="Payment required")
    
    # Create enrollment
    enrollment = Enrollment(
        user_id=current_user.id,
        course_id=course_id,
        purchase_price=course.price if not course.is_free else 0,
        total_lessons=sum(len(m.lessons) for m in course.modules)
    )
    
    db.add(enrollment)
    
    # Update course statistics
    course.enrollment_count += 1
    
    # Send welcome notification
    notification = Notification(
        user_id=current_user.id,
        type="enrollment",
        title="Welcome to the Course!",
        message=f"You've successfully enrolled in '{course.title}'. Start learning now!",
        action_url=f"/learn/{course_id}"
    )
    db.add(notification)
    
    db.commit()
    
    return {"message": "Successfully enrolled", "enrollment_id": enrollment.id}

@router.get("/enrollments", response_model=List[schemas.EnrollmentDetail])
async def get_my_enrollments(
    status: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get user's course enrollments
    """
    query = db.query(Enrollment).filter(Enrollment.user_id == current_user.id)
    
    if status:
        query = query.filter(Enrollment.status == status)
    
    enrollments = query.order_by(Enrollment.enrolled_at.desc()).all()
    
    return enrollments

@router.post("/courses/{course_id}/progress")
async def update_lesson_progress(
    course_id: int,
    lesson_id: int,
    progress_data: schemas.LessonProgressUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update lesson progress for enrolled user
    """
    enrollment = db.query(Enrollment).filter(
        Enrollment.user_id == current_user.id,
        Enrollment.course_id == course_id
    ).first()
    
    if not enrollment:
        raise HTTPException(status_code=403, detail="Not enrolled in this course")
    
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
    progress.progress_percentage = progress_data.progress_percentage
    progress.video_last_position_seconds = progress_data.video_position
    progress.last_accessed_at = datetime.utcnow()
    
    if progress_data.is_completed:
        progress.is_completed = True
        progress.completed_at = datetime.utcnow()
        enrollment.completed_lessons += 1
    
    # Update enrollment progress
    enrollment.progress_percentage = (enrollment.completed_lessons / enrollment.total_lessons) * 100
    enrollment.last_accessed_at = datetime.utcnow()
    
    # Check if course completed
    if enrollment.progress_percentage >= 100:
        enrollment.status = "completed"
        enrollment.completed_at = datetime.utcnow()
        
        # Issue certificate
        certificate = Certificate(
            user_id=current_user.id,
            course_id=course_id,
            enrollment_id=enrollment.id,
            certificate_number=generate_certificate_number(),
            verification_code=generate_verification_code()
        )
        db.add(certificate)
        
        # Send completion notification
        notification = Notification(
            user_id=current_user.id,
            type="certificate",
            title="Congratulations! Course Completed",
            message=f"You've completed the course and earned your certificate!",
            action_url=f"/certificates/{certificate.id}"
        )
        db.add(notification)
    
    db.commit()
    
    return {"message": "Progress updated", "progress": enrollment.progress_percentage}

# ==================== Reviews & Ratings ====================

@router.post("/courses/{course_id}/reviews", response_model=schemas.Review)
async def add_review(
    course_id: int,
    review_data: schemas.ReviewCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Add a review for a course (must be enrolled)
    """
    # Check enrollment
    enrollment = db.query(Enrollment).filter(
        Enrollment.user_id == current_user.id,
        Enrollment.course_id == course_id
    ).first()
    
    if not enrollment:
        raise HTTPException(status_code=403, detail="Must be enrolled to review")
    
    # Check if already reviewed
    existing = db.query(Review).filter(
        Review.user_id == current_user.id,
        Review.course_id == course_id
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Already reviewed this course")
    
    review = Review(
        course_id=course_id,
        user_id=current_user.id,
        **review_data.dict()
    )
    
    db.add(review)
    
    # Update course rating
    course = db.query(Course).filter(Course.id == course_id).first()
    reviews = db.query(Review).filter(Review.course_id == course_id).all()
    
    course.rating = sum(r.rating for r in reviews) / len(reviews)
    course.rating_count = len(reviews)
    
    # Update instructor rating
    for instructor in course.instructors:
        all_instructor_reviews = db.query(Review).join(Course).filter(
            Course.instructors.contains(instructor)
        ).all()
        
        instructor.instructor_rating = sum(r.rating for r in all_instructor_reviews) / len(all_instructor_reviews)
        instructor.instructor_rating_count = len(all_instructor_reviews)
    
    db.commit()
    db.refresh(review)
    
    return review

@router.get("/courses/{course_id}/reviews", response_model=schemas.ReviewListResponse)
async def get_course_reviews(
    course_id: int,
    sort_by: str = Query("helpful", regex="^(helpful|newest|rating_high|rating_low)$"),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """
    Get reviews for a course with sorting and pagination
    """
    query = db.query(Review).filter(Review.course_id == course_id)
    
    # Sorting
    if sort_by == "helpful":
        query = query.order_by(Review.helpful_count.desc())
    elif sort_by == "newest":
        query = query.order_by(Review.created_at.desc())
    elif sort_by == "rating_high":
        query = query.order_by(Review.rating.desc())
    elif sort_by == "rating_low":
        query = query.order_by(Review.rating.asc())
    
    total = query.count()
    reviews = query.offset((page - 1) * limit).limit(limit).all()
    
    # Get rating distribution
    rating_dist = db.query(
        Review.rating,
        db.func.count(Review.id)
    ).filter(Review.course_id == course_id).group_by(Review.rating).all()
    
    return {
        "reviews": reviews,
        "total": total,
        "page": page,
        "pages": (total + limit - 1) // limit,
        "rating_distribution": dict(rating_dist)
    }

# ==================== Wishlist Management ====================

@router.post("/wishlist/{course_id}")
async def add_to_wishlist(
    course_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Add a course to wishlist
    """
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
        raise HTTPException(status_code=400, detail="Already in wishlist")
    
    wishlist_item = Wishlist(
        user_id=current_user.id,
        course_id=course_id
    )
    
    db.add(wishlist_item)
    db.commit()
    
    return {"message": "Added to wishlist"}

@router.delete("/wishlist/{course_id}")
async def remove_from_wishlist(
    course_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Remove a course from wishlist
    """
    wishlist_item = db.query(Wishlist).filter(
        Wishlist.user_id == current_user.id,
        Wishlist.course_id == course_id
    ).first()
    
    if not wishlist_item:
        raise HTTPException(status_code=404, detail="Not in wishlist")
    
    db.delete(wishlist_item)
    db.commit()
    
    return {"message": "Removed from wishlist"}

@router.get("/wishlist", response_model=List[schemas.CourseCard])
async def get_wishlist(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get user's wishlist
    """
    wishlist_items = db.query(Course).join(Wishlist).filter(
        Wishlist.user_id == current_user.id
    ).all()
    
    return wishlist_items

# ==================== Cart Management ====================

@router.post("/cart/{course_id}")
async def add_to_cart(
    course_id: int,
    coupon_code: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Add a course to shopping cart
    """
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    # Check if already in cart
    existing = db.query(CartItem).filter(
        CartItem.user_id == current_user.id,
        CartItem.course_id == course_id
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Already in cart")
    
    # Check if already enrolled
    enrollment = db.query(Enrollment).filter(
        Enrollment.user_id == current_user.id,
        Enrollment.course_id == course_id
    ).first()
    
    if enrollment:
        raise HTTPException(status_code=400, detail="Already enrolled in this course")
    
    # Calculate price with coupon if provided
    final_price = course.price
    discount = 0
    
    if coupon_code:
        coupon = db.query(Coupon).filter(
            Coupon.code == coupon_code,
            Coupon.is_active == True
        ).first()
        
        if coupon and coupon.valid_until > datetime.utcnow():
            if coupon.discount_type == "percentage":
                discount = course.price * (coupon.discount_value / 100)
                if coupon.max_discount_amount:
                    discount = min(discount, coupon.max_discount_amount)
            else:
                discount = coupon.discount_value
            
            final_price = max(0, course.price - discount)
    
    cart_item = CartItem(
        user_id=current_user.id,
        course_id=course_id,
        price=final_price,
        discount_percentage=(discount / course.price * 100) if course.price > 0 else 0,
        coupon_code=coupon_code
    )
    
    db.add(cart_item)
    db.commit()
    
    return {"message": "Added to cart", "final_price": final_price}

@router.get("/cart", response_model=schemas.CartResponse)
async def get_cart(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get user's shopping cart
    """
    cart_items = db.query(CartItem).filter(
        CartItem.user_id == current_user.id
    ).all()
    
    total = sum(item.price for item in cart_items)
    
    return {
        "items": cart_items,
        "total": total,
        "count": len(cart_items)
    }

# ==================== Categories ====================

@router.get("/categories", response_model=List[schemas.Category])
async def get_categories(
    db: Session = Depends(get_db)
):
    """
    Get all course categories with subcategories
    """
    categories = db.query(Category).filter(
        Category.parent_id == None
    ).all()
    
    return categories

# ==================== Helper Functions ====================

def review_course_quality(course_id: int):
    """
    Background task to review course quality before publication
    """
    # Implement automated quality checks
    # - Check video quality
    # - Verify content completeness
    # - Check for inappropriate content
    # - etc.
    pass

def generate_certificate_number():
    """Generate unique certificate number"""
    import uuid
    return f"CERT-{uuid.uuid4().hex[:12].upper()}"

def generate_verification_code():
    """Generate certificate verification code"""
    import uuid
    return uuid.uuid4().hex[:16].upper()