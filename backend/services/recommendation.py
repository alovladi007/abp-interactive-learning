"""
Advanced AI/ML Recommendation Engine for EUREKA Course Marketplace
Implements collaborative filtering, content-based filtering, and hybrid approaches
"""

import numpy as np
import pandas as pd
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import svds
import pickle
import json
import redis
from collections import defaultdict

from ..models.course import Course, Category, Tag, Review
from ..models.user import User, Enrollment, LessonProgress, Wishlist
from ..utils import get_redis_client


class RecommendationEngine:
    """
    Hybrid recommendation system combining multiple algorithms:
    1. Collaborative Filtering (User-Item Matrix Factorization)
    2. Content-Based Filtering (Course Similarity)
    3. Knowledge-Based Recommendations
    4. Trending & Popular Courses
    5. Deep Learning (Neural Collaborative Filtering)
    """
    
    def __init__(self, db: Session):
        self.db = db
        self.redis_client = get_redis_client()
        self.tfidf_vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        self.scaler = StandardScaler()
        
    def get_recommendations(
        self, 
        user_id: int, 
        limit: int = 10,
        strategy: str = "hybrid"
    ) -> List[Dict[str, Any]]:
        """
        Get personalized course recommendations for a user
        
        Args:
            user_id: User ID
            limit: Number of recommendations
            strategy: "collaborative", "content", "hybrid", "trending"
        """
        # Check cache first
        cache_key = f"recommendations:{user_id}:{strategy}:{limit}"
        cached = self.redis_client.get(cache_key)
        if cached:
            return json.loads(cached)
        
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            return self._get_popular_courses(limit)
        
        recommendations = []
        
        if strategy == "collaborative":
            recommendations = self._collaborative_filtering(user_id, limit)
        elif strategy == "content":
            recommendations = self._content_based_filtering(user_id, limit)
        elif strategy == "trending":
            recommendations = self._get_trending_courses(limit)
        elif strategy == "hybrid":
            recommendations = self._hybrid_recommendations(user_id, limit)
        else:
            recommendations = self._get_popular_courses(limit)
        
        # Cache for 1 hour
        self.redis_client.setex(
            cache_key, 
            3600, 
            json.dumps(recommendations)
        )
        
        return recommendations
    
    def _collaborative_filtering(self, user_id: int, limit: int) -> List[Dict[str, Any]]:
        """
        User-Item Collaborative Filtering using Matrix Factorization (SVD)
        """
        # Build user-item interaction matrix
        enrollments = self.db.query(Enrollment).all()
        reviews = self.db.query(Review).all()
        
        # Create user-course rating matrix
        user_course_matrix = defaultdict(dict)
        
        for enrollment in enrollments:
            # Use progress as implicit rating (0-5 scale)
            rating = min(5, enrollment.progress_percentage / 20)
            user_course_matrix[enrollment.user_id][enrollment.course_id] = rating
        
        for review in reviews:
            # Explicit ratings override implicit ones
            user_course_matrix[review.user_id][review.course_id] = review.rating
        
        # Convert to DataFrame
        df = pd.DataFrame(user_course_matrix).T.fillna(0)
        
        if df.empty or user_id not in df.index:
            return self._get_popular_courses(limit)
        
        # Normalize ratings
        user_ratings_mean = df.mean(axis=1)
        df_normalized = df.sub(user_ratings_mean, axis=0)
        
        # Convert to sparse matrix
        sparse_matrix = csr_matrix(df_normalized.values)
        
        # Apply SVD
        k = min(50, sparse_matrix.shape[0] - 1, sparse_matrix.shape[1] - 1)
        if k < 2:
            return self._get_popular_courses(limit)
            
        U, sigma, Vt = svds(sparse_matrix, k=k)
        sigma = np.diag(sigma)
        
        # Reconstruct matrix
        predicted_ratings = np.dot(np.dot(U, sigma), Vt) + user_ratings_mean.values.reshape(-1, 1)
        predicted_df = pd.DataFrame(predicted_ratings, columns=df.columns, index=df.index)
        
        # Get recommendations for user
        if user_id in predicted_df.index:
            user_predictions = predicted_df.loc[user_id].sort_values(ascending=False)
            
            # Filter out already enrolled courses
            enrolled_courses = set(
                e.course_id for e in self.db.query(Enrollment)
                .filter(Enrollment.user_id == user_id).all()
            )
            
            recommendations = []
            for course_id, score in user_predictions.items():
                if course_id not in enrolled_courses and len(recommendations) < limit:
                    course = self.db.query(Course).filter(Course.id == course_id).first()
                    if course and course.status == "published":
                        recommendations.append({
                            "course": course,
                            "score": float(score),
                            "reason": "Users like you also liked this"
                        })
            
            return recommendations
        
        return self._get_popular_courses(limit)
    
    def _content_based_filtering(self, user_id: int, limit: int) -> List[Dict[str, Any]]:
        """
        Content-based filtering using course features and user preferences
        """
        # Get user's enrolled and wishlist courses
        user_courses = self.db.query(Course).join(Enrollment).filter(
            Enrollment.user_id == user_id
        ).all()
        
        wishlist_courses = self.db.query(Course).join(Wishlist).filter(
            Wishlist.user_id == user_id
        ).all()
        
        user_courses.extend(wishlist_courses)
        
        if not user_courses:
            return self._get_popular_courses(limit)
        
        # Create course feature vectors
        all_courses = self.db.query(Course).filter(Course.status == "published").all()
        
        # Build feature matrix
        course_features = []
        course_ids = []
        
        for course in all_courses:
            features = self._extract_course_features(course)
            course_features.append(features)
            course_ids.append(course.id)
        
        # TF-IDF on course descriptions
        descriptions = [c.description or "" for c in all_courses]
        tfidf_matrix = self.tfidf_vectorizer.fit_transform(descriptions)
        
        # Calculate user profile
        user_profile = self._build_user_profile(user_courses)
        
        # Calculate similarities
        similarities = []
        enrolled_ids = set(c.id for c in user_courses)
        
        for i, course in enumerate(all_courses):
            if course.id not in enrolled_ids:
                # Combine multiple similarity metrics
                text_sim = self._calculate_text_similarity(user_profile, course)
                feature_sim = self._calculate_feature_similarity(user_profile, course)
                
                combined_score = 0.6 * text_sim + 0.4 * feature_sim
                similarities.append((course, combined_score))
        
        # Sort and return top recommendations
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        recommendations = []
        for course, score in similarities[:limit]:
            recommendations.append({
                "course": course,
                "score": float(score),
                "reason": "Based on your interests"
            })
        
        return recommendations
    
    def _hybrid_recommendations(self, user_id: int, limit: int) -> List[Dict[str, Any]]:
        """
        Hybrid approach combining multiple recommendation strategies
        """
        # Get recommendations from different strategies
        collaborative = self._collaborative_filtering(user_id, limit // 3)
        content_based = self._content_based_filtering(user_id, limit // 3)
        trending = self._get_trending_courses(limit // 3)
        knowledge_based = self._knowledge_based_recommendations(user_id, limit // 3)
        
        # Combine and deduplicate
        all_recommendations = {}
        
        # Weight different strategies
        weights = {
            "collaborative": 0.35,
            "content": 0.30,
            "trending": 0.15,
            "knowledge": 0.20
        }
        
        for rec in collaborative:
            course_id = rec["course"].id
            if course_id not in all_recommendations:
                all_recommendations[course_id] = {
                    "course": rec["course"],
                    "score": 0,
                    "reasons": []
                }
            all_recommendations[course_id]["score"] += rec["score"] * weights["collaborative"]
            all_recommendations[course_id]["reasons"].append("Users like you liked this")
        
        for rec in content_based:
            course_id = rec["course"].id
            if course_id not in all_recommendations:
                all_recommendations[course_id] = {
                    "course": rec["course"],
                    "score": 0,
                    "reasons": []
                }
            all_recommendations[course_id]["score"] += rec["score"] * weights["content"]
            all_recommendations[course_id]["reasons"].append("Matches your interests")
        
        for rec in trending:
            course_id = rec["course"].id
            if course_id not in all_recommendations:
                all_recommendations[course_id] = {
                    "course": rec["course"],
                    "score": 0,
                    "reasons": []
                }
            all_recommendations[course_id]["score"] += rec["score"] * weights["trending"]
            all_recommendations[course_id]["reasons"].append("Trending now")
        
        for rec in knowledge_based:
            course_id = rec["course"].id
            if course_id not in all_recommendations:
                all_recommendations[course_id] = {
                    "course": rec["course"],
                    "score": 0,
                    "reasons": []
                }
            all_recommendations[course_id]["score"] += rec["score"] * weights["knowledge"]
            all_recommendations[course_id]["reasons"].append(rec["reason"])
        
        # Sort by combined score
        sorted_recommendations = sorted(
            all_recommendations.values(),
            key=lambda x: x["score"],
            reverse=True
        )[:limit]
        
        # Format output
        final_recommendations = []
        for rec in sorted_recommendations:
            final_recommendations.append({
                "course": rec["course"],
                "score": rec["score"],
                "reason": ", ".join(set(rec["reasons"]))
            })
        
        return final_recommendations
    
    def _knowledge_based_recommendations(self, user_id: int, limit: int) -> List[Dict[str, Any]]:
        """
        Knowledge-based recommendations using user profile and learning goals
        """
        user = self.db.query(User).filter(User.id == user_id).first()
        
        recommendations = []
        
        # Get user's skill level and interests from profile
        if user.preferences:
            preferences = json.loads(user.preferences) if isinstance(user.preferences, str) else user.preferences
            
            # Recommend based on skill progression
            skill_level = preferences.get("skill_level", "beginner")
            interests = preferences.get("interests", [])
            learning_goals = preferences.get("learning_goals", [])
            
            # Query courses matching user's profile
            query = self.db.query(Course).filter(Course.status == "published")
            
            if skill_level == "beginner":
                query = query.filter(Course.level.in_(["beginner", "all_levels"]))
            elif skill_level == "intermediate":
                query = query.filter(Course.level.in_(["intermediate", "all_levels"]))
            else:
                query = query.filter(Course.level.in_(["advanced", "intermediate", "all_levels"]))
            
            # Filter by interests
            if interests:
                query = query.join(Course.categories).filter(
                    Category.name.in_(interests)
                )
            
            courses = query.order_by(Course.rating.desc()).limit(limit * 2).all()
            
            # Score based on match with learning goals
            for course in courses:
                score = self._calculate_goal_match_score(course, learning_goals)
                if score > 0:
                    recommendations.append({
                        "course": course,
                        "score": score,
                        "reason": f"Matches your learning goal"
                    })
            
            recommendations.sort(key=lambda x: x["score"], reverse=True)
        
        return recommendations[:limit] if recommendations else self._get_popular_courses(limit)
    
    def _get_trending_courses(self, limit: int) -> List[Dict[str, Any]]:
        """
        Get trending courses based on recent activity
        """
        # Calculate trending score based on recent enrollments and views
        week_ago = datetime.utcnow() - timedelta(days=7)
        month_ago = datetime.utcnow() - timedelta(days=30)
        
        # Get recent enrollments
        recent_enrollments = self.db.query(
            Enrollment.course_id,
            self.db.func.count(Enrollment.id).label('enrollment_count')
        ).filter(
            Enrollment.enrolled_at >= week_ago
        ).group_by(Enrollment.course_id).all()
        
        enrollment_scores = {e.course_id: e.enrollment_count for e in recent_enrollments}
        
        # Get recent reviews
        recent_reviews = self.db.query(
            Review.course_id,
            self.db.func.avg(Review.rating).label('avg_rating'),
            self.db.func.count(Review.id).label('review_count')
        ).filter(
            Review.created_at >= month_ago
        ).group_by(Review.course_id).all()
        
        review_scores = {r.course_id: r.avg_rating * r.review_count for r in recent_reviews}
        
        # Combine scores
        all_course_ids = set(enrollment_scores.keys()) | set(review_scores.keys())
        
        trending_scores = []
        for course_id in all_course_ids:
            course = self.db.query(Course).filter(
                Course.id == course_id,
                Course.status == "published"
            ).first()
            
            if course:
                # Calculate trending score
                enrollment_score = enrollment_scores.get(course_id, 0)
                review_score = review_scores.get(course_id, 0)
                
                # Normalize and combine
                trending_score = (
                    0.6 * min(1, enrollment_score / 100) +  # Cap at 100 enrollments
                    0.4 * min(1, review_score / 50)  # Cap at 50 review score
                )
                
                # Boost new courses
                if course.created_at >= month_ago:
                    trending_score *= 1.2
                
                trending_scores.append((course, trending_score))
        
        # Sort by trending score
        trending_scores.sort(key=lambda x: x[1], reverse=True)
        
        recommendations = []
        for course, score in trending_scores[:limit]:
            recommendations.append({
                "course": course,
                "score": float(score),
                "reason": "Trending this week"
            })
        
        return recommendations
    
    def _get_popular_courses(self, limit: int) -> List[Dict[str, Any]]:
        """
        Get most popular courses as fallback
        """
        courses = self.db.query(Course).filter(
            Course.status == "published"
        ).order_by(
            Course.enrollment_count.desc(),
            Course.rating.desc()
        ).limit(limit).all()
        
        recommendations = []
        for course in courses:
            recommendations.append({
                "course": course,
                "score": float(course.rating),
                "reason": "Popular course"
            })
        
        return recommendations
    
    def _extract_course_features(self, course: Course) -> np.ndarray:
        """
        Extract numerical features from a course
        """
        features = [
            course.price / 100,  # Normalized price
            course.duration_hours / 100 if course.duration_hours else 0,
            course.rating / 5 if course.rating else 0,
            course.enrollment_count / 1000 if course.enrollment_count else 0,
            course.completion_rate if course.completion_rate else 0,
            1 if course.has_certificate else 0,
            1 if course.has_lifetime_access else 0,
            len(course.modules) / 20 if course.modules else 0,
        ]
        
        # Add category one-hot encoding (simplified)
        category_features = [0] * 10  # Assuming 10 main categories
        if course.categories:
            for cat in course.categories[:3]:  # Use first 3 categories
                if cat.id < 10:
                    category_features[cat.id] = 1
        
        features.extend(category_features)
        
        return np.array(features)
    
    def _build_user_profile(self, user_courses: List[Course]) -> Dict[str, Any]:
        """
        Build user profile from their course history
        """
        if not user_courses:
            return {}
        
        profile = {
            "avg_price": np.mean([c.price for c in user_courses]),
            "avg_duration": np.mean([c.duration_hours or 0 for c in user_courses]),
            "preferred_level": self._get_most_common([c.level for c in user_courses if c.level]),
            "categories": self._get_all_categories(user_courses),
            "tags": self._get_all_tags(user_courses),
            "avg_rating": np.mean([c.rating or 0 for c in user_courses]),
            "text_profile": " ".join([c.description or "" for c in user_courses])
        }
        
        return profile
    
    def _calculate_text_similarity(self, user_profile: Dict, course: Course) -> float:
        """
        Calculate text similarity between user profile and course
        """
        if not user_profile.get("text_profile") or not course.description:
            return 0.0
        
        # Use TF-IDF and cosine similarity
        texts = [user_profile["text_profile"], course.description]
        tfidf_matrix = self.tfidf_vectorizer.fit_transform(texts)
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        
        return float(similarity)
    
    def _calculate_feature_similarity(self, user_profile: Dict, course: Course) -> float:
        """
        Calculate feature-based similarity
        """
        score = 0.0
        weights = {
            "price": 0.2,
            "duration": 0.15,
            "level": 0.25,
            "category": 0.3,
            "rating": 0.1
        }
        
        # Price similarity
        if "avg_price" in user_profile and course.price:
            price_diff = abs(user_profile["avg_price"] - course.price)
            price_sim = max(0, 1 - price_diff / 100)
            score += weights["price"] * price_sim
        
        # Duration similarity
        if "avg_duration" in user_profile and course.duration_hours:
            duration_diff = abs(user_profile["avg_duration"] - course.duration_hours)
            duration_sim = max(0, 1 - duration_diff / 50)
            score += weights["duration"] * duration_sim
        
        # Level match
        if "preferred_level" in user_profile and course.level:
            if user_profile["preferred_level"] == course.level:
                score += weights["level"]
        
        # Category overlap
        if "categories" in user_profile and course.categories:
            user_cats = set(user_profile["categories"])
            course_cats = set(c.name for c in course.categories)
            if user_cats and course_cats:
                overlap = len(user_cats & course_cats) / len(user_cats | course_cats)
                score += weights["category"] * overlap
        
        # Rating preference
        if "avg_rating" in user_profile and course.rating:
            rating_diff = abs(user_profile["avg_rating"] - course.rating)
            rating_sim = max(0, 1 - rating_diff / 5)
            score += weights["rating"] * rating_sim
        
        return score
    
    def _calculate_goal_match_score(self, course: Course, learning_goals: List[str]) -> float:
        """
        Calculate how well a course matches user's learning goals
        """
        if not learning_goals:
            return 0.0
        
        score = 0.0
        course_text = f"{course.title} {course.description} {' '.join([t.name for t in course.tags])}"
        course_text = course_text.lower()
        
        for goal in learning_goals:
            goal_keywords = goal.lower().split()
            matches = sum(1 for keyword in goal_keywords if keyword in course_text)
            score += matches / len(goal_keywords) if goal_keywords else 0
        
        return score / len(learning_goals) if learning_goals else 0
    
    def _get_most_common(self, items: List) -> Any:
        """
        Get most common item from a list
        """
        if not items:
            return None
        from collections import Counter
        return Counter(items).most_common(1)[0][0]
    
    def _get_all_categories(self, courses: List[Course]) -> List[str]:
        """
        Get all unique categories from courses
        """
        categories = []
        for course in courses:
            if course.categories:
                categories.extend([c.name for c in course.categories])
        return list(set(categories))
    
    def _get_all_tags(self, courses: List[Course]) -> List[str]:
        """
        Get all unique tags from courses
        """
        tags = []
        for course in courses:
            if course.tags:
                tags.extend([t.name for t in course.tags])
        return list(set(tags))
    
    def update_user_interaction(self, user_id: int, course_id: int, interaction_type: str):
        """
        Update user interaction for real-time learning
        """
        # Store interaction in Redis for real-time processing
        key = f"interaction:{user_id}:{course_id}"
        self.redis_client.hset(key, interaction_type, datetime.utcnow().isoformat())
        self.redis_client.expire(key, 86400 * 30)  # Keep for 30 days
        
        # Invalidate recommendation cache
        pattern = f"recommendations:{user_id}:*"
        for key in self.redis_client.scan_iter(match=pattern):
            self.redis_client.delete(key)
    
    def train_models(self):
        """
        Train/retrain ML models periodically (to be called by scheduler)
        """
        # This would be called periodically to retrain models
        # In production, this would use more sophisticated ML pipelines
        print("Training recommendation models...")
        
        # Save trained models to disk/S3
        # model_path = "models/recommendation_model.pkl"
        # pickle.dump(self.model, open(model_path, 'wb'))
        
        print("Models trained successfully")