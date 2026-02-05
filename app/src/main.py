import os
from fastapi import FastAPI, HTTPException
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response
import redis

app = FastAPI(title="DevOps Hands-on App")

REQUESTS = Counter("app_requests_total", "Total HTTP requests", ["endpoint"])

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_KEY = "hits"

def get_redis_client() -> redis.Redis:
    return redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

@app.get("/health")
def health():
    REQUESTS.labels(endpoint="/health").inc()
    return {"status": "ok"}

@app.get("/hello")
def hello(name: str = "world"):
    REQUESTS.labels(endpoint="/hello").inc()
    return {"message": f"Hello, {name}!"}

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.get("/hits")
def hits():
    """
    Increments a counter in Redis and returns the total.
    This proves multi-container networking works (app -> redis).
    """
    REQUESTS.labels(endpoint="/hits").inc()

    try:
        r = get_redis_client()
        value = r.incr(REDIS_KEY)
        return {"redis_host": REDIS_HOST, "hits": value}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Redis error: {e}")

