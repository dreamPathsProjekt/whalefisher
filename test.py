import docker
import time

from pprint import pprint

client = docker.from_env()

containers = client.containers.list()

while(True):
    pprint(containers)
    time.sleep(2)