#/bin/bash

docker build -t baserow-ac .
docker run -d --rm --name baserow-ac  -p 8020:8020 --env-file secret.env baserow-ac