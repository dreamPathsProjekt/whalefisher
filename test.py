import docker

from pprint import pprint

client = docker.from_env()

containers = client.containers.list()

pprint(containers)