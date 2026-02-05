from fastapi import FastAPI
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response

app = FastAPI(title="DevOps Hands-on App")

REQUESTS = Counter(
    "app_requests_total",
    "Total HTTP requests",
    ["endpoint"]
)

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
    return Response(
        generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )
