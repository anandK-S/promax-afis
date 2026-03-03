# ========================================
# Pro-Max AFIS - Redis Client Configuration
# ========================================
# Redis connection and caching utilities
# Author: Pro-Max Development Team

import redis
import json
import logging
from typing import Optional, Any
from datetime import timedelta

from .config import settings

# Configure logging
logger = logging.getLogger(__name__)


class RedisClient:
    """
    Redis client wrapper for caching and session management
    """
    
    def __init__(self):
        """Initialize Redis client"""
        self.redis_cache = None
        self.redis_session = None
        self._initialize_clients()
    
    def _initialize_clients(self) -> None:
        """Initialize Redis clients with optimized settings"""
        try:
            # Cache Redis client
            self.redis_cache = redis.from_url(
                settings.redis_cache_url,
                encoding="utf-8",
                decode_responses=True,
                socket_connect_timeout=5,
                socket_timeout=5,
                retry_on_timeout=True,
                health_check_interval=30
            )
            
            # Session Redis client
            self.redis_session = redis.from_url(
                settings.redis_url,
                encoding="utf-8",
                decode_responses=True,
                socket_connect_timeout=5,
                socket_timeout=5,
                retry_on_timeout=True,
                health_check_interval=30
            )
            
            # Test connections
            self.redis_cache.ping()
            self.redis_session.ping()
            
            logger.info("Redis clients initialized successfully")
            
        except Exception as e:
            logger.error(f"Redis initialization failed: {str(e)}")
            self.redis_cache = None
            self.redis_session = None
    
    def cache_get(self, key: str) -> Optional[Any]:
        """
        Get value from cache
        
        Args:
            key: Cache key
            
        Returns:
            Cached value or None if not found
        """
        try:
            if not self.redis_cache:
                return None
            
            value = self.redis_cache.get(key)
            if value:
                return json.loads(value)
            return None
            
        except Exception as e:
            logger.error(f"Cache get error for key '{key}': {str(e)}")
            return None
    
    def cache_set(
        self, 
        key: str, 
        value: Any, 
        expire_seconds: Optional[int] = None
    ) -> bool:
        """
        Set value in cache
        
        Args:
            key: Cache key
            value: Value to cache (must be JSON serializable)
            expire_seconds: Expiration time in seconds
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if not self.redis_cache:
                return False
            
            serialized_value = json.dumps(value)
            if expire_seconds:
                self.redis_cache.setex(key, expire_seconds, serialized_value)
            else:
                self.redis_cache.set(key, serialized_value)
            
            return True
            
        except Exception as e:
            logger.error(f"Cache set error for key '{key}': {str(e)}")
            return False
    
    def cache_delete(self, key: str) -> bool:
        """
        Delete key from cache
        
        Args:
            key: Cache key
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if not self.redis_cache:
                return False
            
            self.redis_cache.delete(key)
            return True
            
        except Exception as e:
            logger.error(f"Cache delete error for key '{key}': {str(e)}")
            return False
    
    def cache_clear_pattern(self, pattern: str) -> int:
        """
        Clear all keys matching pattern
        
        Args:
            pattern: Redis key pattern (e.g., "user:*")
            
        Returns:
            Number of keys deleted
        """
        try:
            if not self.redis_cache:
                return 0
            
            keys = self.redis_cache.keys(pattern)
            if keys:
                return self.redis_cache.delete(*keys)
            return 0
            
        except Exception as e:
            logger.error(f"Cache clear pattern error for '{pattern}': {str(e)}")
            return 0
    
    def session_get(self, key: str) -> Optional[str]:
        """
        Get session value
        
        Args:
            key: Session key
            
        Returns:
            Session value or None
        """
        try:
            if not self.redis_session:
                return None
            
            return self.redis_session.get(key)
            
        except Exception as e:
            logger.error(f"Session get error for key '{key}': {str(e)}")
            return None
    
    def session_set(
        self, 
        key: str, 
        value: str, 
        expire_seconds: int = 3600
    ) -> bool:
        """
        Set session value
        
        Args:
            key: Session key
            value: Session value
            expire_seconds: Expiration time in seconds (default: 1 hour)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if not self.redis_session:
                return False
            
            self.redis_session.setex(key, expire_seconds, value)
            return True
            
        except Exception as e:
            logger.error(f"Session set error for key '{key}': {str(e)}")
            return False
    
    def session_delete(self, key: str) -> bool:
        """
        Delete session key
        
        Args:
            key: Session key
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if not self.redis_session:
                return False
            
            self.redis_session.delete(key)
            return True
            
        except Exception as e:
            logger.error(f"Session delete error for key '{key}': {str(e)}")
            return False
    
    def is_connected(self) -> bool:
        """
        Check if Redis clients are connected
        
        Returns:
            True if connected, False otherwise
        """
        try:
            if self.redis_cache:
                self.redis_cache.ping()
                return True
            return False
        except Exception:
            return False


# Global Redis client instance
redis_client = RedisClient()