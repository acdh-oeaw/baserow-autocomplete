from fastapi import FastAPI, HTTPException, Request
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from fastapi_cache.decorator import cache

from acdh_baserow_pyutils import BaseRowClient
from app.config import DATABASES, BASEROW_PW, BASEROW_USER, BASEROW_URL

app = FastAPI()


@app.get("/")
@cache(expire=60 * 60)
async def root(request: Request):
    endpoints = [
        {
            "db_name": x["db_name"],
            "db_id": x["db_id"],
            "endpoint": f"{request.url._url}db/{x['db_id']}",
        }
        for x in DATABASES
    ]

    return {
        "message": "Hello World",
        "docs": f"{request.url._url}docs",
        "endpoints": endpoints,
    }


@app.get("/db/{db_id}")
@cache(expire=60 * 60)
async def list_tables(db_id: str):
    result = None
    db_token = None
    for x in DATABASES:
        if x['db_id'] == db_id:
            result = x
            db_token = x["db_token"]
            break
    if result:
        client = BaseRowClient(BASEROW_USER, BASEROW_PW, db_token, br_base_url=BASEROW_URL)
        tables = client.list_tables(db_id)
        return tables
    else:
        detail_msg = f"no baserow database with ID: <{db_id}> defined in config.py"
        raise HTTPException(status_code=404, detail=detail_msg)


@app.on_event("startup")
async def startup():
    FastAPICache.init(InMemoryBackend())
