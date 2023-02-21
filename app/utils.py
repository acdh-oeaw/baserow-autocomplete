def make_ac_uris(db_id: str, endpoint: str, base_uri: str) -> str:
    uri = f"{base_uri}ac/{db_id}/{endpoint}"
    return uri
