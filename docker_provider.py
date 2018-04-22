import docker


def provide_client(fn):

    def wrapper():
        docker_client = docker.client.from_env()
        result = fn(client=docker_client)
        docker_client.close()

        return result

    return wrapper


@provide_client
def get_client_info(client=None):
    return client.info()


@provide_client
def get_services(client=None):
    return client.services.list()


def get_service_json():
    services = get_services()
    return [dict(id=service.id, name=service.name) for service in services]


@provide_client
def get_nodes(client=None):
    return client.nodes.list()


def get_node_json():

    nodes = get_nodes()
    nodes_list = []

    for node in nodes:
        nodes_dict = dict(id=node.id,
                          hostname=node.attrs['Description']['Hostname'],
                          ip=node.attrs['Status']['Addr'])
        nodes_list.append(nodes_dict)

    return nodes_list


@provide_client
def get_containers(client=None):
    return client.containers.list()


def get_container_json():

    containers = get_containers()
    return [dict(id=container.id,
                 name=container.name)
            for container in containers]