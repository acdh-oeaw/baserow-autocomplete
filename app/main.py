from fastapi import FastAPI, HTTPException, Request
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from fastapi_cache.decorator import cache

from acdh_baserow_pyutils import BaseRowClient
from app.config import DATABASES, BASEROW_PW, BASEROW_USER, BASEROW_URL
from app.utils import make_ac_uris

app = FastAPI()


@app.get("/")
async def root(request: Request):
    endpoints = [
        {
            "db_name": x["db_name"],
            "db_id": db_key,
            "endpoint": f"{request.url._url}db/{db_key}/tables",
            "autocompletes": [make_ac_uris(db_key, key, request.url._url) for key, value in x["endpoints"].items()]
        }
        for db_key, x in DATABASES.items()
    ]

    return {
        "message": "A baserow autocomplete service",
        "docs": f"{request.url._url}docs",
        "endpoints": endpoints,
    }


@app.get("/ac/{db_id}/{endpoint}")
async def query_endpoint(db_id: str, endpoint: str):
    try:
        cur_db = DATABASES[db_id]
    except KeyError:
        detail_msg = f"no baserow database with ID: <{db_id}> defined in config.py"
        raise HTTPException(status_code=404, detail=detail_msg)
    return cur_db["endpoints"][endpoint]


@app.get("/db/{db_id}/tables")
@cache(expire=60 * 60)
async def list_tables(request: Request, db_id: str):
    result = []
    try:
        cur_db = DATABASES[db_id]
    except KeyError:
        detail_msg = f"no baserow database with ID: <{db_id}> defined in config.py"
        raise HTTPException(status_code=404, detail=detail_msg)
    client = BaseRowClient(BASEROW_USER, BASEROW_PW, "db_token", br_base_url=BASEROW_URL)
    tables = client.list_tables(cur_db["db_id"])
    for x in tables:
        item = x
        item["fields"] = f"{request.url._url}/{x['id']}/fields"
        result.append(item)
    return result


@app.get("/db/{db_id}/tables/{table_id}/fields")
@cache(expire=60 * 60)
async def list_ac_fields(db_id: str, table_id: str):
    client = BaseRowClient(BASEROW_USER, BASEROW_PW, "db_token", br_base_url=BASEROW_URL)
    result = client.list_fields(table_id)
    return result


@app.on_event("startup")
async def startup():
    FastAPICache.init(InMemoryBackend())
