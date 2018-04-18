import docker
import time

from pprint import pprint

def get_services(client):
    return client.services.list()

def get_service_names(client):
    services = get_services(client)
    return [service.name for service in services]

def task_names(client, service_name):
    # return [service. service in get_services(client)]
    pass




if __name__ == "__main__":
    client = docker.from_env()

    while(True):
        pprint(get_service_names(client))
        time.sleep(2)