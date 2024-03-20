#!/bin/bash

api_name=${1:-"transcriptor-api"}
image_name=${2:-"${api_name}-image"}
image_tag=${3:-"1.0"}
container_name=${4:-"${api_name}-container"}

docker container prune -f

docker run \
    -p 80:8000/tcp \
    -e environment=hml \
    --name ${container_name} \
    ${image_name}:${image_tag} \
    uvicorn main.entrypoint.main:app --host 0.0.0.0 --port 8000
