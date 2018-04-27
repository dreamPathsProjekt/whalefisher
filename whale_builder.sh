#!/bin/bash

docker build -t whalefisher-manager ./whalefisher-manager/ && \
docker tag whalefisher-manager  registry.dream:5001/whalefisher-manager:"$1" && \
docker tag whalefisher-manager  registry.dream:5001/whalefisher-manager:latest && \
docker push registry.dream:5001/whalefisher-manager:"$1" && \
docker push registry.dream:5001/whalefisher-manager:latest

docker build -t whalefisher-data_provider ./whalefisher-data_provider/ && \
docker tag whalefisher-data_provider  registry.dream:5001/whalefisher-data_provider:"$1" && \
docker tag whalefisher-data_provider  registry.dream:5001/whalefisher-data_provider:latest && \
docker push registry.dream:5001/whalefisher-data_provider:"$1" && \
docker push registry.dream:5001/whalefisher-data_provider:latest

# docker stack deploy --compose-file whale-fisher.yml whalefisher
exit 0
