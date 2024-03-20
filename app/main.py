import requests
from typing import Union
from fastapi import FastAPI, HTTPException, Request
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from fastapi_cache.decorator import cache

from acdh_baserow_pyutils import BaseRowClient
from app.config import DATABASES, BASEROW_PW, BASEROW_USER, BASEROW_URL
from app.utils import make_ac_uris, populate_baserow_response
from app.zotero_utils import populate_zotero_response


app = FastAPI()


@app.get("/")
async def root(request: Request):
    endpoints = [
        {
            "db_name": x["db_name"],
            "db_id": db_key,
            "endpoint": f"{request.url._url}db/{db_key}/tables",
            "autocompletes": [
                make_ac_uris(db_key, key, request.url._url)
                for key, _ in x["endpoints"].items()
            ],
        }
        for db_key, x in DATABASES.items()
    ]
    for x in endpoints:
        db_key = x["db_id"]
        print(db_key)
        try:
            DATABASES[db_key]["zotero"]
            print("###################")
        except KeyError:
            continue
        zotero_ep = make_ac_uris(db_key, "zotero", request.url._url)
        x["autocompletes"].append(zotero_ep)

    return {
        "message": "A baserow autocomplete service",
        "docs": f"{request.url._url}docs",
        "endpoints": endpoints,
    }


@app.get("/ac/{db_id}/{endpoint}")
async def query_endpoint(
    db_id: str, endpoint: str, q: str, format: Union[str, None] = "teicompleter"
):
    try:
        cur_db = DATABASES[db_id]
    except KeyError:
        detail_msg = f"no baserow database with ID: <{db_id}> defined in config.py"
        raise HTTPException(status_code=404, detail=detail_msg)
    if endpoint == "zotero":
        zotero_api = cur_db["zotero"]
        url = f"{zotero_api}?q={q}"
        r = requests.get(url)
        data = r.json()
        result = populate_zotero_response(data, format=format)
        return result
    cur_conf = cur_db["endpoints"][endpoint]
    br_table_id = cur_conf["table_id"]
    query_field_id = cur_conf["search_field_id"]
    client = BaseRowClient(
        BASEROW_USER, BASEROW_PW, "db_token", br_base_url=BASEROW_URL
    )
    data = client.search_rows(br_table_id, q, query_field_id, lookup_type="contains")
    result = populate_baserow_response(cur_conf, data, format=format)
    return result


@app.get("/db/{db_id}/tables")
@cache(expire=60 * 60)
async def list_tables(request: Request, db_id: str):
    result = []
    try:
        cur_db = DATABASES[db_id]
    except KeyError:
        detail_msg = f"no baserow database with ID: <{db_id}> defined in config.py"
        raise HTTPException(status_code=404, detail=detail_msg)
    client = BaseRowClient(
        BASEROW_USER, BASEROW_PW, "db_token", br_base_url=BASEROW_URL
    )
    tables = client.list_tables(cur_db["db_id"])
    for x in tables:
        item = x
        item["fields"] = f"{request.url._url}/{x['id']}/fields"
        result.append(item)
    return result


@app.get("/db/{db_id}/tables/{table_id}/fields")
@cache(expire=60 * 60)
async def list_ac_fields(db_id: str, table_id: str):
    client = BaseRowClient(
        BASEROW_USER, BASEROW_PW, "db_token", br_base_url=BASEROW_URL
    )
    result = client.list_fields(table_id)
    return result


@app.on_event("startup")
async def startup():
    FastAPICache.init(InMemoryBackend())
