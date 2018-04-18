import docker
import time

from pprint import pprint

def get_services(client):
    return client.services.list()

def get_service_json(client):
    services = get_services(client)
    return [dict(id = service.id, name = service.name) for service in services]

def get_nodes(client):
    return client.nodes.list()

def get_node_json(client):
    nodes = get_nodes(client)
    nodes_list = []

    for node in nodes:
        nodes_dict = dict(id = node.id,
                          name = node.attrs['Spec']['Name'],
                          hostname = node.attrs['Description']['Hostname'],
                          ip = node.attrs['Status']['Addr'])
        nodes_list.append(nodes_dict)

    return nodes_list


def get_containers(client):
    return client.containers.list()

def get_container_json(client):
    containers = get_containers(client)
    return [dict(id = container.id, name = container.name)  for container in containers]

def task_names(client, service_name):
    # return [service. service in get_services(client)]
    pass




if __name__ == "__main__":

    while True:
        client = docker.from_env()

        print("Services")
        pprint(get_service_json(client))
        print("\n")

        print("Containers")
        pprint(get_container_json(client))
        print("\n")

        print("Nodes")
        [ pprint(node.attrs) for node in get_nodes(client) ]
        print("=============\n")

        time.sleep(15)
