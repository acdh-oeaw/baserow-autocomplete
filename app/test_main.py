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
        endpoints = response.json()["endpoints"]
        assert len(endpoints) == len(DATABASES)


def test_ac_endpoint():
    db_id = "test"
    endpoints = [key for key, _ in DATABASES[db_id]["endpoints"].items()]
    for x in endpoints:
        with TestClient(app) as client:
            response = client.get(f"/ac/{db_id}/{x}")
            assert response.status_code == 422
            response = client.get(f"/ac/{db_id}/{x}?q=A")
            assert response.status_code == 200


def test_nonexiting_ac_endpoint():
    with TestClient(app) as client:
        response = client.get("/ac/quatsch/blödsinn?q=A")
        assert response.status_code == 404


def test_list_tables_endpoint():
    db_id = "test"
    with TestClient(app) as client:
        response = client.get(f"/db/{db_id}/tables")
        assert response.status_code == 200
    with TestClient(app) as client:
        response = client.get("/db/blödsinn/tables")
        assert response.status_code == 404
