from fastapi import FastAPI, Request
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from fastapi_cache.decorator import cache

from app.config import DATABASES

app = FastAPI()


@app.get("/")
@cache(expire=60 * 60)
async def root(request: Request):
    endpoints = [
        {
            "db_name": x["db_name"],
            "db_id": x["db_id"],
            "endpoint": f"{request.url._url}{x['db_id']}",
        }
        for x in DATABASES
    ]

    return {
        "message": "Hello World",
        "docs": f"{request.url._url}docs",
        "endpoints": endpoints,
    }


@app.on_event("startup")
async def startup():
    FastAPICache.init(InMemoryBackend())
