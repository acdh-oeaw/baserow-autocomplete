#/bin/bash

echo "Be aware that we are ignoring warnings, this might come back to you one day!"
coverage run -m pytest -v -p no:warnings 
coverage report
coverage html
xdg-open ./htmlcov/index.html