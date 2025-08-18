import redis.asyncio as redis
from typing import Optional, Any, Union
import json
import pickle
from datetime import datetime, timedelta
from app.core.config import settings
import hashlib
import logging

logger = logging.getLogger(__name__)

class RedisCache:
    def __init__(self):
        self.redis: Optional[redis.Redis] = None
        
    async def connect(self):
        """Initialize Redis connection pool."""
        self.redis = await redis.from_url(
            str(settings.REDIS_URL),
            encoding="utf-8",
            decode_responses=settings.REDIS_DECODE_RESPONSES,
            max_connections=settings.REDIS_POOL_SIZE,
        )
        
    async def disconnect(self):
        """Close Redis connection."""
        if self.redis:
            await self.redis.close()
    
    def _make_key(self, *args) -> str:
        """Generate cache key from arguments."""
        key_parts = [str(arg) for arg in args]
        return ":".join(key_parts)
    
    async def get(self, key: str, default: Any = None) -> Any:
        """Get value from cache."""
        try:
            value = await self.redis.get(key)
            if value is None:
                return default
            # Try to deserialize JSON
            try:
                return json.loads(value)
            except (json.JSONDecodeError, TypeError):
                return value
        except Exception as e:
            logger.error(f"Cache get error: {e}")
            return default
    
    async def set(
        self, 
        key: str, 
        value: Any, 
        expire: Optional[int] = None,
        nx: bool = False,
        xx: bool = False
    ) -> bool:
        """Set value in cache with optional expiration."""
        try:
            # Serialize to JSON if possible
            if isinstance(value, (dict, list)):
                value = json.dumps(value)
            
            return await self.redis.set(
                key, 
                value, 
                ex=expire or settings.CACHE_TTL,
                nx=nx,
                xx=xx
            )
        except Exception as e:
            logger.error(f"Cache set error: {e}")
            return False
    
    async def delete(self, *keys: str) -> int:
        """Delete keys from cache."""
        try:
            return await self.redis.delete(*keys)
        except Exception as e:
            logger.error(f"Cache delete error: {e}")
            return 0
    
    async def exists(self, *keys: str) -> int:
        """Check if keys exist."""
        return await self.redis.exists(*keys)
    
    async def incr(self, key: str, amount: int = 1) -> int:
        """Increment counter."""
        return await self.redis.incr(key, amount)
    
    async def decr(self, key: str, amount: int = 1) -> int:
        """Decrement counter."""
        return await self.redis.decr(key, amount)
    
    async def expire(self, key: str, seconds: int) -> bool:
        """Set expiration on key."""
        return await self.redis.expire(key, seconds)
    
    async def ttl(self, key: str) -> int:
        """Get time to live for key."""
        return await self.redis.ttl(key)
    
    # Exposure control methods
    def exposure_key(self, question_id: int, version: int) -> str:
        """Generate exposure control key."""
        day = datetime.utcnow().strftime("%Y%m%d")
        return f"exp:{day}:{question_id}:{version}"
    
    async def can_serve(self, question_id: int, version: int) -> bool:
        """Check if question can be served based on exposure limits."""
        if not settings.EXPOSURE_CONTROL_ENABLED:
            return True
        
        key = self.exposure_key(question_id, version)
        count = await self.get(key, 0)
        return int(count) < settings.MAX_DAILY_EXPOSURES
    
    async def bump_exposure(self, question_id: int, version: int) -> None:
        """Increment exposure count for question."""
        if not settings.EXPOSURE_CONTROL_ENABLED:
            return
        
        key = self.exposure_key(question_id, version)
        pipe = self.redis.pipeline()
        pipe.incr(key, 1)
        pipe.expire(key, 86400)  # 24 hours
        await pipe.execute()
    
    # Session management
    async def get_session(self, session_id: str) -> Optional[dict]:
        """Get session data."""
        key = f"session:{session_id}"
        return await self.get(key)
    
    async def set_session(
        self, 
        session_id: str, 
        data: dict, 
        expire: int = 7200
    ) -> bool:
        """Set session data with expiration."""
        key = f"session:{session_id}"
        return await self.set(key, data, expire=expire)
    
    # Rate limiting
    async def check_rate_limit(
        self, 
        identifier: str, 
        limit: int, 
        window: int
    ) -> tuple[bool, int]:
        """Check if rate limit is exceeded."""
        key = f"rate_limit:{identifier}"
        
        try:
            pipe = self.redis.pipeline()
            pipe.incr(key)
            pipe.expire(key, window)
            results = await pipe.execute()
            
            current_count = results[0]
            return current_count <= limit, current_count
        except Exception as e:
            logger.error(f"Rate limit check error: {e}")
            return True, 0
    
    # Caching decorator
    def cache_result(
        self, 
        prefix: str, 
        expire: Optional[int] = None,
        key_builder: Optional[callable] = None
    ):
        """Decorator for caching function results."""
        def decorator(func):
            async def wrapper(*args, **kwargs):
                # Build cache key
                if key_builder:
                    cache_key = key_builder(*args, **kwargs)
                else:
                    # Simple key from function name and args
                    key_data = f"{func.__name__}:{args}:{kwargs}"
                    key_hash = hashlib.md5(key_data.encode()).hexdigest()
                    cache_key = f"{prefix}:{key_hash}"
                
                # Try to get from cache
                cached = await self.get(cache_key)
                if cached is not None:
                    return cached
                
                # Execute function
                result = await func(*args, **kwargs)
                
                # Store in cache
                await self.set(cache_key, result, expire=expire)
                
                return result
            return wrapper
        return decorator

# Global cache instance
cache = RedisCache()