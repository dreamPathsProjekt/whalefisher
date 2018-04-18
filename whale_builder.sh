#!/bin/bash

docker build -t whalefisher . && \
docker tag whalefisher  registry.greece:5001/whalefisher:"$1" && \
docker tag whalefisher  registry.greece:5001/whalefisher:latest && \
docker push registry.greece:5001/whalefisher:"$1" && \
docker push registry.greece:5001/whalefisher:latest
docker service update whalefisher_exporter --force --image registry.greece:5001/whalefisher:"$1"
# docker stack deploy --compose-file whale-fisher.yml whalefisher
exit 0
