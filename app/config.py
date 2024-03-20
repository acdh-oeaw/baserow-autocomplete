import os

BASEROW_URL = "https://baserow.acdh-dev.oeaw.ac.at/api/"
BASEROW_USER = os.environ.get("BASEROW_USER")
BASEROW_PW = os.environ.get("BASEROW_PW")

DATABASES = {
    "test":
    {
        "db_name": "Test DB",
        "db_id": "538",
        "endpoints": {
            "persons": {
                "table_id": "3284",
                "search_field_name": "name",
                "search_field_id": "29742",
                "id_field_name": "project_id"
            },
            "places": {
                "table_id": "3285",
                "search_field_name": "name",
                "search_field_id": "29745",
                "id_field_name": "project_id"
            }
        },
        "zotero": "https://api.zotero.org/groups/1085708/items"
    },
    "emt":
    {
        "db_name": "EMT",
        "db_id": "278",
        "endpoints": {
            "persons": {
                "table_id": "1513",
                "search_field_name": "name",
                "search_field_id": "12741",
                "id_field_name": "emt_id",
            },
            "places": {
                "table_id": "1514",
                "search_field_name": "name",
                "search_field_id": "12745",
                "id_field_name": "emt_id",
            },
        },
    },
    "amp":
    {
        "db_name": "AMP",
        "db_id": "274",
        "endpoints": {
            "persons": {
                "table_id": "1484",
                "search_field_name": "name",
                "search_field_id": "12492",
                "id_field_name": "amp_id",
            },
            "places": {
                "table_id": "1483",
                "search_field_name": "name",
                "search_field_id": "12489",
                "id_field_name": "amp_id",
            },
        },
    },
    "frd":
    {
        "db_name": "Freud Edition",
        "db_id": "270",
        "endpoints": {
            "persons": {
                "table_id": "1474",
                "search_field_name": "name",
                "search_field_id": "12428",
                "id_field_name": "frd_id",
            },
            "places": {
                "table_id": "1468",
                "search_field_name": "name",
                "search_field_id": "12396",
                "id_field_name": "frd_id",
            },
        },
    },
    "b-vg":
    {
        "db_name": "bundesverfassung",
        "db_id": "421",
        "endpoints": {
            "persons": {
                "table_id": "2290",
                "search_field_name": "name",
                "search_field_id": "20812",
                "id_field_name": "bv_id",
            },
            "document": {
                "table_id": "2289",
                "search_field_name": "doc_title",
                "search_field_id": "20804",
                "id_field_name": "bv_id",
            },
        },
    },
}
