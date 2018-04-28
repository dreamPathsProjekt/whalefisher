import docker
import time
import os
import requests

from pprint import pprint
import json

def get_services(client):
    return client.services.list()


def get_service_json(client):
    services = get_services(client)
    return [dict(id=service.id, name=service.name) for service in services]


def get_nodes(client):
    return client.nodes.list()


def get_node_json(client):
    nodes = get_nodes(client)
    nodes_list = []

    for node in nodes:
        nodes_dict = dict(id=node.id,
                          hostname=node.attrs['Description']['Hostname'],
                          ip=node.attrs['Status']['Addr'])
        nodes_list.append(nodes_dict)

    return nodes_list


def get_containers(client):
    return client.containers.list()


def get_container_json(client):
    containers = get_containers(client)
    return [dict(id=container.id,
                 name=container.name)
            for container in containers]


def task_names(client, service_name):
    # return [service. service in get_services(client)]
    pass


if __name__ == "__main__":

    # tls_config = docker.tls.TLSConfig(
    # client_cert=('/path/to/client-cert.pem', '/path/to/client-key.pem')
    # )

    client = docker.client.from_env()
    # pprint(os.environ)
    print('Test ')
    req_get_name = requests.get('http://10.132.0.2:8080/container')

    cont_id = ''
    for container in req_get_name.json():
        if str(container['name']).startswith('whale_whalefisher-data_provider'):
            cont_id = container['id']

    request_stream = requests.get('http://10.132.0.2:8080/container/{}/logs/stream'.format(cont_id), stream=True)

    for char in request_stream.iter_content(chunk_size=1000, decode_unicode=False):
        line = ''
        while str(char) != '\n':
            line += str(char)
        print(line)
    # request1 = requests.get('http://10.132.0.11:8086/node/current')
    # request2 = requests.get('http://10.132.0.28:8086/node/current')

    # request3 = requests.get('http://10.132.0.11:8085/node/current')
    # request4 = requests.get('http://10.132.0.28:8085/node/current')

    # print('Test Providers')
    # # pprint(request.status_code)
    # print('it-docker-m1')
    # pprint(request1.json())

    # print('\n')
    # print('it-docker-m2')
    # pprint(request2.json())
    # print('\n')

    # print('Test Manager')
    # # pprint(request.status_code)
    # print('it-docker-m1')
    # pprint(request3.json())

    # print('\n')
    # print('it-docker-m2')
    # pprint(request4.json())
    # print('\n')
    # # pprint(request.headers)
    # request1.close()
    # request2.close()
    # request3.close()
    # request4.close()

    # pprint(client.info())
        # print("Services")
        # pprint(get_service_json(client))
        # print("\n")

        # print("Containers")
        # pprint(get_container_json(client))
        # print("\n")

        # print("Nodes")
        # pprint(get_node_json(client))
        # print("=============\n")

        # # Test Log output
        # tmp = get_containers(client)[1]

        # # stream means that lines are b'', may need to decode
        # logs = tmp.logs(stream=True)

        # [print(str(log, 'utf-8').strip()) for log in logs]

        # time.sleep(15)
