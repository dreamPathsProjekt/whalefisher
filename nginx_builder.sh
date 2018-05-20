#!/bin/bash

# Edit below line to your own private registry
DOCKER_REGISTRY=registry.dream:5001

SECRET_USERNAME="$(docker secret ls | grep  "whale_username" | awk '{ print $2 }')"
SECRET_PASSWORD="$(docker secret ls | grep  "whale_password" | awk '{ print $2 }')"

if [ "$SECRET_USERNAME" != "whale_username" ]
then
    read -rp 'Please type username: ' WHALE_USERNAME
    echo "$WHALE_USERNAME" | docker secret create whale_username -
fi

if [ "$SECRET_PASSWORD" != "whale_password" ]
then
    read -srp 'Please type your password: ' WHALE_PASSWORD
    echo "$WHALE_PASSWORD" | docker secret create whale_password -
fi

read -rp 'Build image & push? y to proceed: ' BUILD_PROMPT

if [ "$BUILD_PROMPT" == "y" ]
then
    docker build -t nginx-proxy ./nginx-proxy/ && \
    docker tag nginx-proxy  $DOCKER_REGISTRY/nginx-proxy:"$1" && \
    docker tag nginx-proxy  $DOCKER_REGISTRY/nginx-proxy:latest && \
    docker push $DOCKER_REGISTRY/nginx-proxy:"$1" && \
    docker push $DOCKER_REGISTRY/nginx-proxy:latest
fi