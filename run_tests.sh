#/bin/bash

coverage run -m pytest -v
coverage report
coverage html
xdg-open ./htmlcov/index.html