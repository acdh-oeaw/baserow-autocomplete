import os

BASEROW_URL = "https://baserow.acdh-dev.oeaw.ac.at/api/"
BASEROW_USER = os.environ.get('BASEROW_USER')
BASEROW_PW = os.environ.get('BASEROW_PW')

DATABASES = [
    {
        "db_name": "EMT",
        "db_id": "278",
        "db_token": "gRV2yDuNk44mUmsqxkqWULNcEIope7kZ"
    },
    {
        "db_name": "AMP",
        "db_id": "274",
        "db_token": "NtEzsa1wy9vdNpGWIRXFt0WJHvPu1UVV"
    },
    {
        "db_name": "GrocerIST",
        "db_id": "275",
        "db_token": "hZSU3Tc6CwchKG4Eq41gZmglUs5YA99V"
    },
]
