def make_ac_uris(db_id: str, endpoint: str, base_uri: str) -> str:
    uri = f"{base_uri}ac/{db_id}/{endpoint}"
    return uri


def populate_baserow_response(
    cur_config: dict, data: dict, format: str = "teicompleter"
) -> dict:
    project_id = cur_config["id_field_name"]
    search_field_name = cur_config["search_field_name"]
    if format == "select2":
        result = {
            "results": [],
        }
        for x in data["results"]:
            item = {"id": f"#{x[project_id]}", "text": x[search_field_name]}
            result["results"].append(item)

        return result

    elif format == "original":
        return {"results": data}

    else:
        result = {"tc:suggestion": []}
        for x in data["results"]:
            item = {"tc:value": f"#{x[project_id]}", "tc:description": x[search_field_name]}
            result["tc:suggestion"].append(item)

        return result
