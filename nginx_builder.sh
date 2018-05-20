#!/bin/bash

# Edit below line to your own private registry
DOCKER_REGISTRY=registry.dream:5001

read -rp 'Please type username: ' WHALE_USERNAME
read -srp 'Please type your password: ' WHALE_PASSWORD

echo "$WHALE_USERNAME" | docker secret create whale_username -
echo "$WHALE_PASSWORD" | docker secret create whale_password -

docker build -t nginx-proxy ./nginx-proxy/ && \
docker tag nginx-proxy  $DOCKER_REGISTRY/nginx-proxy:"$1" && \
docker tag nginx-proxy  $DOCKER_REGISTRY/nginx-proxy:latest && \
docker push $DOCKER_REGISTRY/nginx-proxy:"$1" && \
docker push $DOCKER_REGISTRY/nginx-proxy:latest