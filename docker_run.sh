#!/bin/bash

api_name=${1:-"transcriptior-api"}
image_name=${1:-"${api_name}-image"}
image_tag=${2:-"1.0"}
container_name=${3:-"${api_name}-container"}

docker container prune -f

docker run \
    -p 80:8000/tcp \
    -e environment=hml \
    --name ${container_name} \
    ${image_name}:${image_tag} \
    uvicorn main.entrypoint.main:app --host 0.0.0.0 --port 8000
