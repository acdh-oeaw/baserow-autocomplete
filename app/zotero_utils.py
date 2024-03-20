def zotero_description(item_data: dict) -> dict:
    item_title = item_data.get('title', 'no title provided')
    item_place = item_data.get('place', 'no place provided')
    item_date = item_data.get('date', 'no date provided')
    item_id = f"#zotero_{item_data['key']}"
    item_description = f"{item_title}, {item_place}, {item_date}"
    return {
        "id": item_id,
        "value": item_description
    }


def populate_zotero_response(data: list, format: str = "teicompleter") -> dict:
    if format == 'select2':
        result = {
            "results": [],
        }
        for x in data:
            item_data = zotero_description(x['data'])
            item = {
                "id": item_data['id'],
                "text": item_data['value']
            }
            result['results'].append(item)
        return result

    elif format == 'original':
        return {
            "result": data
        }
    else:
        result = {
            "tc:suggestion": []
        }
        for x in data:
            item_data = zotero_description(x['data'])
            item = {
                "tc:value": item_data['id'],
                "tc:description": item_data['value']
            }
            result['tc:suggestion'].append(item)
        return result
