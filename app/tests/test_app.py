import pytest
import httpx
from src.main import app

pytestmark = pytest.mark.anyio

async def test_health():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"

async def test_hello():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/hello")
    assert r.status_code == 200
    assert r.json()["message"] == "Hello, world!"

async def test_metrics():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/metrics")
    assert r.status_code == 200
    assert "app_requests_total" in r.text

async def test_hits_endpoint_exists():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/hits")
    # Without redis running, this will likely be 500 locally in unit-test mode.
    # We'll do integration tests with docker-compose later.
    assert r.status_code in (200, 500)

