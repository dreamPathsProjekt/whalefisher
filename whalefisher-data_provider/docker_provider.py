import docker
import os

def provide_client(fn):

    def wrapper(*args, **kwargs):
        docker_client = docker.client.from_env(version='auto')
        result = fn(client=docker_client, *args, **kwargs)
        docker_client.close()

        return result

    return wrapper


def get_current_nodename():
    return dict(current=os.environ['DOCKER_NODE'])


# @provide_client
# def get_nodes(client=None):
#     return client.nodes.list()


# @provide_client
# def get_node_by_id(id, client=None):
#     return client.nodes.get(id)


# def get_node_json():

#     nodes = get_nodes()
#     nodes_list = []

#     for node in nodes:
#         nodes_dict = dict(id=node.id,
#                           availability=node.attrs['Spec']['Availability'],
#                           hostname=node.attrs['Description']['Hostname'],
#                           ip=node.attrs['Status']['Addr'],  # use this to filter containers
#                           labels=node.attrs['Spec']['Labels'])
#         nodes_list.append(nodes_dict)

#     return nodes_list


@provide_client
def get_containers(client=None):
    return client.containers.list()


def get_container_json():

    containers = get_containers()
    return [dict(id=container.id,
                 name=container.name)
            for container in containers]


@provide_client
def get_container_by_id(id, client=None):
    return client.containers.get(id)


def get_container_json_by_id(id):

    container = get_container_by_id(id)
    return dict(id=container.id, name=container.name)
