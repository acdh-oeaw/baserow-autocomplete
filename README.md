[![codecov](https://codecov.io/github/acdh-oeaw/baserow-autocomplete/branch/main/graph/badge.svg?token=HQFFN8LPEE)](https://codecov.io/github/acdh-oeaw/baserow-autocomplete)
[![Test](https://github.com/acdh-oeaw/baserow-autocomplete/actions/workflows/test.yml/badge.svg)](https://github.com/acdh-oeaw/baserow-autocomplete/actions/workflows/test.yml)
[![flake8 Lint](https://github.com/acdh-oeaw/baserow-autocomplete/actions/workflows/lint.yml/badge.svg)](https://github.com/acdh-oeaw/baserow-autocomplete/actions/workflows/lint.yml)

# baserow-autocomplete
generic web-service to expose baserow data via common autocomplete formats


## install

* clone the repo
* install python-packes (`pip install -r requirements.txt`), ideally in some virtual env
* provide your baserow credentials via environment variables (see e.g. `dev.env`)
* start the server (see `startserver.sh`)

## config

modify `./app/config.py` to your needs

## docker

* `docker build -t baserow-ac .`
* `docker run -d --name baserow-ac -p 8020:8020 --env-file secret.env baserow-ac`

