import os
import redis
import json

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = os.getenv("REDIS_PORT", 6379)

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

CACHE_HITS_KEY = "cache:hits"
CACHE_MISSES_KEY = "cache:misses"

def generate_cache_key(model, prompt):
    return f"Eval:{model}:{prompt}"

def get_cached_response(model, prompt):
    key = generate_cache_key(model, prompt)
    cached_response = redis_client.get(key)
    if cached_response:
        redis_client.incr(CACHE_HITS_KEY)
        return json.loads(cached_response)
    
    redis_client.incr(CACHE_MISSES_KEY)
    return None

def set_cached_response(model, prompt, data, ttl = 3600):
    key = generate_cache_key(model, prompt)
    redis_client.setex(key, ttl, json.dumps(data))

def get_cache_stats():
    hits = int(redis_client.get(CACHE_HITS_KEY) or 0)
    misses = int(redis_client.get(CACHE_MISSES_KEY) or 0)
    total_keys = len(redis_client.keys("eval:*"))
    memory_info = redis_client.info("memory")

    hit_rate = 0
    if hits + misses > 0:
        hit_rate = hits / (hits + misses)

    return {
        "total_cached_items": total_keys,
        "cache_hits": hits,
        "cache_misses": misses,
        "hit_rate": round(hit_rate, 4),
        "memory_used_bytes": memory_info.get("used_memory", 0)
    }