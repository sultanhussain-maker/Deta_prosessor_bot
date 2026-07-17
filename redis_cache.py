# app/cache/redis_cache.py
import redis, hashlib
from app.utils.security import REDIS_URL

r = redis.from_url(REDIS_URL)

def make_key(content: bytes):
    return "file:" + hashlib.sha256(content).hexdigest()

def get_cached_report(content: bytes):
    k = make_key(content)
    val = r.get(k)
    return val.decode() if val else None
#
#
def set_cached_report(content: bytes, report: str):
    k = make_key(content)
    r.set(k, report, ex=3600)