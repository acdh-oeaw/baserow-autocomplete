from fastapi.testclient import TestClient
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend

from .main import app
from .config import DATABASES


@app.on_event("startup")
async def startup():
    FastAPICache.init(InMemoryBackend())


def test_read_main():
    with TestClient(app) as client:
        response = client.get("/")
        assert response.status_code == 200


def test_correct_endpoint_number():
    with TestClient(app) as client:
        response = client.get("/")
        endpoints = response.json()['endpoints']
        assert len(endpoints) == len(DATABASES)
