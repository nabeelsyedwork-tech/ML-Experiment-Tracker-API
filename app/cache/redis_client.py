import redis
from app.core.config import settings

redis_client = redis.StrictRedis(host=settings.REDIS_HOST,port=settings.REDIS_PORT,decode_responses=True)

def get_redis_client():
    return redis_client