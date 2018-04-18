#!/bin/bash

docker build -t whalefisher . && \
docker tag whalefisher  registry.dream:5001/whalefisher:"$1" && \
docker tag whalefisher  registry.dream:5001/whalefisher:latest && \
docker push registry.dream:5001/whalefisher:"$1" && \
docker push registry.dream:5001/whalefisher:latest

# docker stack deploy --compose-file whale-fisher.yml whalefisher
exit 0
