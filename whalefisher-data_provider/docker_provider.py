import docker
import os


def provide_client(fn):

    def wrapper(*args, **kwargs):
        docker_client = docker.client.from_env()
        result = fn(client=docker_client, *args, **kwargs)
        docker_client.close()

        return result

    return wrapper


def get_current_nodename():
    return dict(current=os.environ['DOCKER_NODE'])


@provide_client
def get_client_info(client=None):
    return client.info()


@provide_client
def get_services(client=None):
    return client.services.list()


def get_all_services_by_name(service_name):
    services = get_services()
    result = []

    for service in services:

        if service_name in service.name:
            result.append(service)

    return result


# Requires unique name
def get_service_by_name(service_name):
    services = get_services()

    for service in services:

        if service_name == service.name:
            return service

    return None


# def get_service_json():
#     services = get_services()

#     for service in services:
#         service_dict = dict(id=service.id,
#                             name=service.name)

#         service_doc = Document(
#                 data=service_dict,
#                 links=Collection(Link)
#             )
#     return [service_doc for service in services]


def get_service_json_by_name(service_name):
    services = get_all_services_by_name(service_name)
    return [dict(id=service.id, name=service.name) for service in services]


def get_running_tasks(service_name):
    service = get_service_by_name(service_name)

    if service is not None:
        return service.tasks(filters={"desired-state": "running"})

    return []


def get_tasks_json(tasks, service_name_input):
    task_list = []

    if len(tasks) != 0:

        for task in tasks:

            node_name_by_id = get_node_by_id(id=task['NodeID']).attrs['Description']['Hostname']

            task_dict = dict(
                id=task['ID'],
                node_id=task['NodeID'],
                node_name=node_name_by_id,
                service_id=task['ServiceID'],
                service_name=service_name_input,
                desired_state=task['DesiredState'],
                current_state=task['Status']['State'],
                slot=task['Slot'] if 'Slot' in task.keys() else None
            )
            task_list.append(task_dict)

    return task_list


@provide_client
def get_nodes(client=None):
    return client.nodes.list()


@provide_client
def get_node_by_id(id, client=None):
    return client.nodes.get(id)


def get_node_json():

    nodes = get_nodes()
    nodes_list = []

    for node in nodes:
        nodes_dict = dict(id=node.id,
                          availability=node.attrs['Spec']['Availability'],
                          hostname=node.attrs['Description']['Hostname'],
                          ip=node.attrs['Status']['Addr'],  # use this to filter containers
                          labels=node.attrs['Spec']['Labels'])
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


@provide_client
def get_container_by_id(id, client=None):
    return client.containers.get(id)


def get_container_json_by_id(id):

    container = get_container_by_id(id)
    return dict(id=container.id, name=container.name)
