#!/bin/bash

# Edit below line to your own private registry
DOCKER_REGISTRY=registry.dream:5001

docker build -t whalefisher-manager ./whalefisher-manager/ && \
docker tag whalefisher-manager  $DOCKER_REGISTRY/whalefisher-manager:"$1" && \
docker tag whalefisher-manager  $DOCKER_REGISTRY/whalefisher-manager:latest && \
docker push $DOCKER_REGISTRY/whalefisher-manager:"$1" && \
docker push $DOCKER_REGISTRY/whalefisher-manager:latest

docker build -t whalefisher-data_provider ./whalefisher-data_provider/ && \
docker tag whalefisher-data_provider  $DOCKER_REGISTRY/whalefisher-data_provider:"$1" && \
docker tag whalefisher-data_provider  $DOCKER_REGISTRY/whalefisher-data_provider:latest && \
docker push $DOCKER_REGISTRY/whalefisher-data_provider:"$1" && \
docker push $DOCKER_REGISTRY/whalefisher-data_provider:latest

# docker stack deploy --compose-file whale-fisher.yml whalefisher
exit 0
