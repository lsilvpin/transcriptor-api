#!/bin/bash

api_name=${1:-"transcriptior-api"}
image_name=${1:-"${api_name}-image"}
image_tag=${2:-"1.0"}

docker build \
    -t ${image_name}:${image_tag} \
    -f ./Base.Dockerfile \
    .
