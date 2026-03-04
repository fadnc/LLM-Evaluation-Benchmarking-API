import os
import redis
import json

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = os.getenv("REDIS_PORT", 6379)

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

def generate_cache_key(model, prompt):
    return f"{model}_{prompt}"

def get_cached_response(model, prompt):
    cache_key = generate_cache_key(model, prompt)
    key = generate_cache_key(model, prompt)
    cached_response = redis_client.get(key)
    if cached_response:
        return json.loads(cached_response)
    return None

def set_cached_response(model, prompt, data, ttl = 3600):
    key = generate_cache_key(model, prompt)
    redis_client.setex(key, ttl, json.dumps(data))