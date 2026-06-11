import redis
import logging
import time
from typing import Optional
from app.core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("CacheService")

class CacheService:
    def __init__(self):
        self.redis_client = None
        self.memory_cache = {}
        try:
            # Connect to Redis
            self.redis_client = redis.Redis(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=0,
                socket_connect_timeout=2,
                decode_responses=True
            )
            # Test connection
            self.redis_client.ping()
            logger.info("Successfully connected to Redis instance.")
        except Exception as e:
            logger.warning(
                f"Redis connection failed ({e}). Falling back to fully typed local in-memory dict cache for this development cycle."
            )
            self.redis_client = None

    def get(self, key: str) -> Optional[str]:
        if self.redis_client:
            try:
                return self.redis_client.get(key)
            except Exception as e:
                logger.error(f"Redis GET failed: {e}")
        # Local mock cache lookup
        cache_item = self.memory_cache.get(key)
        if cache_item:
            # Check if key is expired
            if cache_item["expire_at"] > time.time():
                return cache_item["value"]
            else:
                del self.memory_cache[key]
        return None

    def set(self, key: str, value: str, expire: int = 300) -> None:
        if self.redis_client:
            try:
                self.redis_client.set(key, value, ex=expire)
                return
            except Exception as e:
                logger.error(f"Redis SET failed: {e}")
        # Local mock cache storage
        self.memory_cache[key] = {
            "value": value,
            "expire_at": time.time() + expire
        }

    def delete(self, key: str) -> None:
        if self.redis_client:
            try:
                self.redis_client.delete(key)
                return
            except Exception as e:
                logger.error(f"Redis DELETE failed: {e}")
        if key in self.memory_cache:
            del self.memory_cache[key]

cache_service = CacheService()
