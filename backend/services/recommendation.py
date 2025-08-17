"""Advanced Recommendation Service for EUREKA Course Marketplace"""
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import TruncatedSVD
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_, desc
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import pickle
import os
import logging

from models.course import Course, Category, Tag
from models.enrollment import Enrollment, WatchHistory, Wishlist, LessonProgress
from models.user import User, UserPreference

logger = logging.getLogger(__name__)

class RecommendationService:
    """Advanced recommendation engine using hybrid approach"""
    
    def __init__(self):
        self.model_path = "models/recommendation_model.pkl"
        self.content_model = None
        self.collaborative_model = None
        self.tfidf_vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        self.svd_model = TruncatedSVD(n_components=50)
        self._load_models()
    
    def _load_models(self):
        """Load pre-trained recommendation models"""
        if os.path.exists(self.model_path):
            try:
                with open(self.model_path, 'rb') as f:
                    models = pickle.load(f)
                    self.content_model = models.get('content')
                    self.collaborative_model = models.get('collaborative')
                logger.info("Recommendation models loaded successfully")
            except Exception as e:
                logger.error(f"Error loading models: {str(e)}")
    
    async def get_recommendations(
        self,
        user_id: int,
        limit: int = 10,
        db: Session = None,
        strategy: str = "hybrid"
    ) -> List[Dict[str, Any]]:
        """Get personalized course recommendations for a user"""
        try:
            # Get user profile and history
            user_profile = await self._get_user_profile(user_id, db)
            
            # Get different types of recommendations
            content_recs = []
            collaborative_recs = []
            trending_recs = []
            
            if strategy in ["content", "hybrid"]:
                content_recs = await self._content_based_recommendations(
                    user_profile, limit * 2, db
                )
            
            if strategy in ["collaborative", "hybrid"]:
                collaborative_recs = await self._collaborative_filtering(
                    user_id, limit * 2, db
                )
            
            if strategy == "hybrid":
                trending_recs = await self._get_trending_courses(limit, db)
            
            # Combine and rank recommendations
            recommendations = self._combine_recommendations(
                content_recs,
                collaborative_recs,
                trending_recs,
                user_profile,
                limit
            )
            
            # Filter out already enrolled courses
            enrolled_ids = await self._get_enrolled_course_ids(user_id, db)
            recommendations = [
                rec for rec in recommendations 
                if rec["id"] not in enrolled_ids
            ][:limit]
            
            # Add personalization scores
            recommendations = await self._add_personalization_scores(
                recommendations, user_profile, db
            )
            
            return recommendations
        
        except Exception as e:
            logger.error(f"Error getting recommendations: {str(e)}")
            # Fallback to popular courses
            return await self._get_popular_courses(limit, db)
    
    async def _get_user_profile(self, user_id: int, db: Session) -> Dict[str, Any]:
        """Build comprehensive user profile for recommendations"""
        profile = {
            "user_id": user_id,
            "skill_level": "beginner",
            "interests": [],
            "completed_courses": [],
            "in_progress_courses": [],
            "preferred_categories": [],
            "preferred_instructors": [],
            "average_course_duration": 0,
            "price_sensitivity": "medium",
            "learning_pace": "normal",
            "interaction_history": []
        }
        
        try:
            # Get user data
            user = db.query(User).filter(User.id == user_id).first()
            if user:
                profile["skill_level"] = user.skill_level or "beginner"
                
                # Get user preferences
                preferences = db.query(UserPreference).filter(
                    UserPreference.user_id == user_id
                ).first()
                
                if preferences:
                    profile["interests"] = preferences.interests or []
                    profile["preferred_categories"] = preferences.preferred_categories or []
            
            # Analyze enrollment history
            enrollments = db.query(Enrollment).filter(
                Enrollment.user_id == user_id
            ).all()
            
            for enrollment in enrollments:
                if enrollment.status == "completed":
                    profile["completed_courses"].append(enrollment.course_id)
                elif enrollment.status == "active":
                    profile["in_progress_courses"].append(enrollment.course_id)
                
                # Track preferred instructors
                if enrollment.course and enrollment.course.instructor_id:
                    profile["preferred_instructors"].append(
                        enrollment.course.instructor_id
                    )
            
            # Analyze viewing patterns
            watch_history = db.query(WatchHistory).filter(
                WatchHistory.user_id == user_id
            ).order_by(desc(WatchHistory.watched_at)).limit(50).all()
            
            for history in watch_history:
                profile["interaction_history"].append({
                    "course_id": history.course_id,
                    "watched_at": history.watched_at,
                    "duration": history.duration,
                    "completion": history.completion_percentage
                })
            
            # Calculate learning patterns
            if enrollments:
                total_duration = sum(
                    e.course.duration_hours for e in enrollments 
                    if e.course and e.course.duration_hours
                )
                profile["average_course_duration"] = total_duration / len(enrollments)
                
                # Determine learning pace
                active_enrollments = [e for e in enrollments if e.status == "active"]
                if active_enrollments:
                    avg_progress_rate = sum(
                        e.progress_percentage / max(
                            (datetime.utcnow() - e.enrolled_at).days, 1
                        )
                        for e in active_enrollments
                    ) / len(active_enrollments)
                    
                    if avg_progress_rate > 5:
                        profile["learning_pace"] = "fast"
                    elif avg_progress_rate < 2:
                        profile["learning_pace"] = "slow"
                
                # Determine price sensitivity
                paid_courses = [
                    e for e in enrollments 
                    if e.payment_amount and e.payment_amount > 0
                ]
                if paid_courses:
                    avg_price = sum(e.payment_amount for e in paid_courses) / len(paid_courses)
                    if avg_price < 30:
                        profile["price_sensitivity"] = "high"
                    elif avg_price > 100:
                        profile["price_sensitivity"] = "low"
            
            return profile
        
        except Exception as e:
            logger.error(f"Error building user profile: {str(e)}")
            return profile
    
    async def _content_based_recommendations(
        self,
        user_profile: Dict[str, Any],
        limit: int,
        db: Session
    ) -> List[Dict[str, Any]]:
        """Generate content-based recommendations"""
        try:
            # Get courses user has interacted with
            interacted_courses = (
                user_profile["completed_courses"] + 
                user_profile["in_progress_courses"]
            )
            
            if not interacted_courses:
                # Use user interests for cold start
                return await self._recommend_by_interests(
                    user_profile["interests"],
                    limit,
                    db
                )
            
            # Get course features
            courses = db.query(Course).filter(
                Course.id.in_(interacted_courses)
            ).all()
            
            if not courses:
                return []
            
            # Build feature matrix
            course_features = []
            for course in courses:
                features = f"{course.title} {course.description} "
                features += f"{course.category.name if course.category else ''} "
                features += " ".join(course.skills_gained or [])
                features += " ".join([tag.name for tag in course.tags])
                course_features.append(features)
            
            # Calculate TF-IDF vectors
            tfidf_matrix = self.tfidf_vectorizer.fit_transform(course_features)
            
            # Get all available courses
            all_courses = db.query(Course).filter(
                Course.status == "published",
                ~Course.id.in_(interacted_courses)
            ).all()
            
            # Calculate similarity scores
            recommendations = []
            for candidate in all_courses:
                candidate_features = f"{candidate.title} {candidate.description} "
                candidate_features += f"{candidate.category.name if candidate.category else ''} "
                candidate_features += " ".join(candidate.skills_gained or [])
                candidate_features += " ".join([tag.name for tag in candidate.tags])
                
                candidate_vector = self.tfidf_vectorizer.transform([candidate_features])
                similarity = cosine_similarity(tfidf_matrix, candidate_vector).mean()
                
                recommendations.append({
                    "id": candidate.id,
                    "score": float(similarity),
                    "reason": "content_similarity",
                    **candidate.to_dict()
                })
            
            # Sort by similarity score
            recommendations.sort(key=lambda x: x["score"], reverse=True)
            
            return recommendations[:limit]
        
        except Exception as e:
            logger.error(f"Error in content-based recommendations: {str(e)}")
            return []
    
    async def _collaborative_filtering(
        self,
        user_id: int,
        limit: int,
        db: Session
    ) -> List[Dict[str, Any]]:
        """Generate collaborative filtering recommendations"""
        try:
            # Build user-item interaction matrix
            enrollments = db.query(
                Enrollment.user_id,
                Enrollment.course_id,
                Enrollment.rating_given
            ).filter(
                Enrollment.rating_given.isnot(None)
            ).all()
            
            if not enrollments:
                return []
            
            # Create DataFrame
            df = pd.DataFrame(enrollments, columns=['user_id', 'course_id', 'rating'])
            
            # Create pivot table
            user_item_matrix = df.pivot_table(
                index='user_id',
                columns='course_id',
                values='rating',
                fill_value=0
            )
            
            # Apply SVD for dimensionality reduction
            user_features = self.svd_model.fit_transform(user_item_matrix)
            
            # Find similar users
            if user_id not in user_item_matrix.index:
                return []
            
            user_idx = user_item_matrix.index.get_loc(user_id)
            user_vector = user_features[user_idx].reshape(1, -1)
            
            # Calculate similarities with other users
            similarities = cosine_similarity(user_vector, user_features)[0]
            similar_users_idx = similarities.argsort()[-10:][::-1]
            similar_users = user_item_matrix.index[similar_users_idx].tolist()
            
            # Get courses liked by similar users
            recommended_courses = set()
            for similar_user in similar_users:
                if similar_user == user_id:
                    continue
                
                liked_courses = db.query(Enrollment).filter(
                    Enrollment.user_id == similar_user,
                    Enrollment.rating_given >= 4.0
                ).all()
                
                for enrollment in liked_courses:
                    recommended_courses.add(enrollment.course_id)
            
            # Filter out already enrolled courses
            enrolled = db.query(Enrollment.course_id).filter(
                Enrollment.user_id == user_id
            ).all()
            enrolled_ids = {e[0] for e in enrolled}
            
            recommended_courses = recommended_courses - enrolled_ids
            
            # Get course details and create recommendations
            recommendations = []
            courses = db.query(Course).filter(
                Course.id.in_(recommended_courses)
            ).all()
            
            for course in courses:
                recommendations.append({
                    "id": course.id,
                    "score": float(similarities[similar_users_idx[0]]),
                    "reason": "collaborative_filtering",
                    **course.to_dict()
                })
            
            recommendations.sort(key=lambda x: x["score"], reverse=True)
            
            return recommendations[:limit]
        
        except Exception as e:
            logger.error(f"Error in collaborative filtering: {str(e)}")
            return []
    
    async def _get_trending_courses(
        self,
        limit: int,
        db: Session
    ) -> List[Dict[str, Any]]:
        """Get trending courses based on recent activity"""
        try:
            # Calculate trending score based on recent enrollments and views
            week_ago = datetime.utcnow() - timedelta(days=7)
            
            trending_query = db.query(
                Course,
                func.count(Enrollment.id).label('recent_enrollments'),
                func.avg(CourseReview.rating).label('avg_rating')
            ).outerjoin(
                Enrollment,
                and_(
                    Course.id == Enrollment.course_id,
                    Enrollment.enrolled_at >= week_ago
                )
            ).outerjoin(
                CourseReview,
                Course.id == CourseReview.course_id
            ).filter(
                Course.status == "published"
            ).group_by(Course.id)
            
            trending_courses = trending_query.order_by(
                desc('recent_enrollments')
            ).limit(limit).all()
            
            recommendations = []
            for course, enrollments, rating in trending_courses:
                # Calculate trending score
                score = enrollments * 0.7
                if rating:
                    score += rating * 0.3
                
                recommendations.append({
                    "id": course.id,
                    "score": float(score),
                    "reason": "trending",
                    **course.to_dict()
                })
            
            return recommendations
        
        except Exception as e:
            logger.error(f"Error getting trending courses: {str(e)}")
            return []
    
    async def _recommend_by_interests(
        self,
        interests: List[str],
        limit: int,
        db: Session
    ) -> List[Dict[str, Any]]:
        """Recommend courses based on user interests"""
        try:
            if not interests:
                return []
            
            # Find courses matching interests
            query = db.query(Course).filter(Course.status == "published")
            
            # Match by category
            categories = db.query(Category).filter(
                Category.name.in_(interests)
            ).all()
            
            if categories:
                category_ids = [c.id for c in categories]
                query = query.filter(Course.category_id.in_(category_ids))
            
            # Match by tags
            tags = db.query(Tag).filter(
                Tag.name.in_(interests)
            ).all()
            
            if tags:
                query = query.join(Course.tags).filter(
                    Tag.id.in_([t.id for t in tags])
                )
            
            # Order by rating and popularity
            courses = query.order_by(
                desc(Course.average_rating),
                desc(Course.total_students)
            ).limit(limit).all()
            
            recommendations = []
            for course in courses:
                recommendations.append({
                    "id": course.id,
                    "score": float(course.average_rating),
                    "reason": "interest_match",
                    **course.to_dict()
                })
            
            return recommendations
        
        except Exception as e:
            logger.error(f"Error recommending by interests: {str(e)}")
            return []
    
    def _combine_recommendations(
        self,
        content_recs: List[Dict],
        collaborative_recs: List[Dict],
        trending_recs: List[Dict],
        user_profile: Dict,
        limit: int
    ) -> List[Dict[str, Any]]:
        """Combine recommendations from different strategies"""
        try:
            # Weight different recommendation types based on user profile
            weights = self._calculate_weights(user_profile)
            
            # Combine all recommendations
            all_recs = {}
            
            # Add content-based recommendations
            for rec in content_recs:
                course_id = rec["id"]
                if course_id not in all_recs:
                    all_recs[course_id] = rec
                    all_recs[course_id]["final_score"] = 0
                all_recs[course_id]["final_score"] += rec["score"] * weights["content"]
            
            # Add collaborative filtering recommendations
            for rec in collaborative_recs:
                course_id = rec["id"]
                if course_id not in all_recs:
                    all_recs[course_id] = rec
                    all_recs[course_id]["final_score"] = 0
                all_recs[course_id]["final_score"] += rec["score"] * weights["collaborative"]
            
            # Add trending recommendations
            for rec in trending_recs:
                course_id = rec["id"]
                if course_id not in all_recs:
                    all_recs[course_id] = rec
                    all_recs[course_id]["final_score"] = 0
                all_recs[course_id]["final_score"] += rec["score"] * weights["trending"]
            
            # Sort by final score
            recommendations = list(all_recs.values())
            recommendations.sort(key=lambda x: x.get("final_score", 0), reverse=True)
            
            # Add diversity
            recommendations = self._add_diversity(recommendations, limit)
            
            return recommendations[:limit]
        
        except Exception as e:
            logger.error(f"Error combining recommendations: {str(e)}")
            return []
    
    def _calculate_weights(self, user_profile: Dict) -> Dict[str, float]:
        """Calculate weights for different recommendation strategies"""
        weights = {
            "content": 0.4,
            "collaborative": 0.4,
            "trending": 0.2
        }
        
        # Adjust weights based on user profile
        if len(user_profile["completed_courses"]) < 3:
            # New user - rely more on trending
            weights["trending"] = 0.5
            weights["content"] = 0.3
            weights["collaborative"] = 0.2
        elif len(user_profile["completed_courses"]) > 10:
            # Experienced user - rely more on personalization
            weights["content"] = 0.45
            weights["collaborative"] = 0.45
            weights["trending"] = 0.1
        
        return weights
    
    def _add_diversity(
        self,
        recommendations: List[Dict],
        limit: int
    ) -> List[Dict[str, Any]]:
        """Add diversity to recommendations"""
        try:
            diverse_recs = []
            seen_categories = set()
            seen_instructors = set()
            
            for rec in recommendations:
                # Check for diversity
                category = rec.get("category", {}).get("id")
                instructor = rec.get("instructor", {}).get("id")
                
                # Prioritize diversity in early recommendations
                if len(diverse_recs) < limit // 2:
                    if category not in seen_categories:
                        diverse_recs.append(rec)
                        seen_categories.add(category)
                        seen_instructors.add(instructor)
                else:
                    # Allow some repetition in later recommendations
                    diverse_recs.append(rec)
                
                if len(diverse_recs) >= limit:
                    break
            
            # Fill remaining slots if needed
            if len(diverse_recs) < limit:
                for rec in recommendations:
                    if rec not in diverse_recs:
                        diverse_recs.append(rec)
                        if len(diverse_recs) >= limit:
                            break
            
            return diverse_recs
        
        except Exception as e:
            logger.error(f"Error adding diversity: {str(e)}")
            return recommendations
    
    async def _add_personalization_scores(
        self,
        recommendations: List[Dict],
        user_profile: Dict,
        db: Session
    ) -> List[Dict[str, Any]]:
        """Add personalization scores and explanations"""
        try:
            for rec in recommendations:
                # Calculate match score
                match_score = 0
                explanations = []
                
                # Skill level match
                if rec.get("level") == user_profile["skill_level"]:
                    match_score += 0.2
                    explanations.append("Matches your skill level")
                
                # Category match
                if rec.get("category", {}).get("id") in user_profile["preferred_categories"]:
                    match_score += 0.3
                    explanations.append("In your preferred category")
                
                # Instructor match
                if rec.get("instructor", {}).get("id") in user_profile["preferred_instructors"]:
                    match_score += 0.2
                    explanations.append("From an instructor you like")
                
                # Duration preference
                duration = rec.get("duration_hours", 0)
                avg_duration = user_profile["average_course_duration"]
                if avg_duration > 0 and abs(duration - avg_duration) < 5:
                    match_score += 0.1
                    explanations.append("Similar duration to your preferences")
                
                # Price sensitivity
                price = rec.get("price", 0)
                if user_profile["price_sensitivity"] == "high" and price < 30:
                    match_score += 0.1
                    explanations.append("Budget-friendly")
                elif user_profile["price_sensitivity"] == "low" and price > 50:
                    match_score += 0.1
                    explanations.append("Premium quality")
                
                # Learning pace match
                if user_profile["learning_pace"] == "fast" and duration < 10:
                    match_score += 0.1
                    explanations.append("Quick to complete")
                elif user_profile["learning_pace"] == "slow" and duration > 20:
                    match_score += 0.1
                    explanations.append("Comprehensive coverage")
                
                rec["personalization_score"] = min(match_score, 1.0)
                rec["explanations"] = explanations[:3]  # Top 3 explanations
            
            return recommendations
        
        except Exception as e:
            logger.error(f"Error adding personalization scores: {str(e)}")
            return recommendations
    
    async def _get_enrolled_course_ids(self, user_id: int, db: Session) -> set:
        """Get IDs of courses user is enrolled in"""
        try:
            enrollments = db.query(Enrollment.course_id).filter(
                Enrollment.user_id == user_id
            ).all()
            return {e[0] for e in enrollments}
        except Exception as e:
            logger.error(f"Error getting enrolled courses: {str(e)}")
            return set()
    
    async def _get_popular_courses(self, limit: int, db: Session) -> List[Dict[str, Any]]:
        """Fallback to popular courses"""
        try:
            courses = db.query(Course).filter(
                Course.status == "published"
            ).order_by(
                desc(Course.average_rating),
                desc(Course.total_students)
            ).limit(limit).all()
            
            return [
                {
                    "id": course.id,
                    "score": float(course.average_rating),
                    "reason": "popular",
                    **course.to_dict()
                }
                for course in courses
            ]
        except Exception as e:
            logger.error(f"Error getting popular courses: {str(e)}")
            return []
    
    async def track_view(self, user_id: int, course_id: int, db: Session):
        """Track course view for recommendation improvement"""
        try:
            watch_history = WatchHistory(
                user_id=user_id,
                course_id=course_id,
                watched_at=datetime.utcnow()
            )
            db.add(watch_history)
            db.commit()
        except Exception as e:
            logger.error(f"Error tracking view: {str(e)}")
    
    async def train_models(self, db: Session):
        """Train recommendation models with latest data"""
        try:
            logger.info("Starting model training...")
            
            # Train content-based model
            await self._train_content_model(db)
            
            # Train collaborative filtering model
            await self._train_collaborative_model(db)
            
            # Save models
            models = {
                'content': self.content_model,
                'collaborative': self.collaborative_model
            }
            
            os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
            with open(self.model_path, 'wb') as f:
                pickle.dump(models, f)
            
            logger.info("Model training completed successfully")
        
        except Exception as e:
            logger.error(f"Error training models: {str(e)}")
    
    async def _train_content_model(self, db: Session):
        """Train content-based filtering model"""
        # Implementation for training content model
        pass
    
    async def _train_collaborative_model(self, db: Session):
        """Train collaborative filtering model"""
        # Implementation for training collaborative model
        pass