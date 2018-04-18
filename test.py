import docker
import time

from pprint import pprint

def get_services(client):
    return client.services.list()

def get_service_json(client):
    services = get_services(client)
    return [dict(id = service.id, name = service.name) for service in services]

def get_containers(client):
    return client.containers.list()

def get_container_json(client):
    containers = get_containers(client)
    return [dict(id = container.id, name = container.name)  for container in containers]

def task_names(client, service_name):
    # return [service. service in get_services(client)]
    pass




if __name__ == "__main__":
    client = docker.from_env()
    print("Services")
    pprint(get_service_json(client))
    print("\n")
    print("Containers")
    pprint(get_container_json(client))
    print("\n")