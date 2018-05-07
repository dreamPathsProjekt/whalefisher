from flask import Flask
from flask import jsonify
from flask import Response
from flask import make_response
from flask import abort
from flask import url_for

from docker import client
import json
import time
import os


# from flask_socketio import SocketIO
# import eventlet
import requests

from docker_provider import *


# eventlet.monkey_patch()
app = Flask(__name__)
# Redirect with or without slashes
app.url_map.strict_slashes = False

# socketio = SocketIO(app, async_mode='eventlet')
URL_PREFIX = '{}:{}'.format(os.environ['EXT_DOMAIN_NAME'], os.environ['PUBLISH_PORT'])


@app.route('/')
def list_routes():
    result = []

    for route in app.url_map.iter_rules():
        result.append({
            'methods': list(route.methods),
            'route': str(route)
        })

    return jsonify({'routes': result, 'total': len(result)})


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


@app.route('/error')
def test_error_handler():
    return abort(404)


@app.route('/bad_request')
def test_bad_request():
    return abort(400)


@app.route('/service')
def get_services_route():
    services = get_service_json()

    return jsonify([{
        'id': service['id'],
        'name': service['name'],
        '_links': {
            'self': URL_PREFIX + url_for('get_services_by_service_name', name=service['name']),
            'tasks': URL_PREFIX + url_for('get_tasks_by_service_name', name=service['name']),
            'logs': {
                'stream': URL_PREFIX + url_for('get_service_logs', name=service['name'])
            }
        }
    } for service in services])


@app.route('/service/<string:name>')
def get_services_by_service_name(name):

    services = get_service_json_by_name(name)

    if len(services) == 0:
        abort(404)

    return jsonify([{
        'id': service['id'],
        'name': service['name'],
        '_links': {
            '_self': URL_PREFIX + url_for('get_services_by_service_name', name=service['name']),
            'tasks': URL_PREFIX + url_for('get_tasks_by_service_name', name=service['name']),
            'logs': {
                'stream': URL_PREFIX + url_for('get_service_logs', name=service['name'])
            }
        }
    } for service in services])


# Requires exact name
@app.route('/service/<string:name>/tasks')
def get_tasks_by_service_name(name):

    tasks = get_tasks_json(tasks=get_running_tasks(name), service_name_input=name)

    if len(tasks) == 0:
        abort(404)

    return jsonify([{
        'id': task['id'],
        'node_id': task['node_id'],
        'node_name': task['node_name'],
        'service_id': task['service_id'],
        'service_name': task['service_name'],
        'desired_state': task['desired_state'],
        'current_state': task['current_state'],
        'slot': task['slot'],
        '_links': {
            '_self': URL_PREFIX + url_for('get_tasks_by_id', name=task['service_name'], id=task['id']),
            'service': URL_PREFIX + url_for('get_services_by_service_name', name=task['service_name']),
            'logs': {
                'json': URL_PREFIX + url_for('get_logs_by_task_id', name=task['service_name'], id=task['id']),
                'compact': URL_PREFIX + url_for('get_logs_by_task_id_compact', name=task['service_name'], id=task['id']),
                'stream': URL_PREFIX + url_for('get_logs_by_task_id_stream', name=task['service_name'], id=task['id'])
            }
        }
    } for task in tasks])


@app.route('/service/<string:name>/tasks/<string:id>')
def get_tasks_by_id(name, id):

    tasks = get_tasks_json(tasks=get_running_tasks(name, task_id=id), service_name_input=name)

    if len(tasks) == 0:
        abort(404)

    if len(tasks) > 1:
        return jsonify({'message': 'Multiple Tasks Found'})

    return jsonify(
        {
            'id': tasks[0]['id'],
            'node_id': tasks[0]['node_id'],
            'node_name': tasks[0]['node_name'],
            'service_id': tasks[0]['service_id'],
            'service_name': tasks[0]['service_name'],
            'desired_state': tasks[0]['desired_state'],
            'current_state': tasks[0]['current_state'],
            'slot': tasks[0]['slot'],
            '_links': {
                '_self': URL_PREFIX + url_for('get_tasks_by_id', name=tasks[0]['service_name'], id=tasks[0]['id']),
                'service': URL_PREFIX + url_for('get_services_by_service_name', name=tasks[0]['service_name']),
                'logs': {
                    'json': URL_PREFIX + url_for('get_logs_by_task_id', name=tasks[0]['service_name'], id=tasks[0]['id']),
                    'compact': URL_PREFIX + url_for('get_logs_by_task_id_compact', name=tasks[0]['service_name'], id=tasks[0]['id']),
                    'stream': URL_PREFIX + url_for('get_logs_by_task_id_stream', name=tasks[0]['service_name'], id=tasks[0]['id'])
                }
            }
        }
    )


@app.route('/service/<string:name>/tasks/<string:id>/logs')
def get_logs_by_task_id(name, id):
    cont_json = get_container_by_task_id(name, id)

    if cont_json is None:
        abort(404)

    request_json = requests.get('http://{}:{}/container/{}/logs'.format(
        cont_json['node_ip'],
        cont_json['node_port'],
        cont_json['container_id']))

    return jsonify(request_json.json())


@app.route('/service/<string:name>/tasks/<string:id>/logs/compact')
def get_logs_by_task_id_compact(name, id):
    cont_json = get_container_by_task_id(name, id)

    if cont_json is None:
        abort(404)

    request_json = requests.get('http://{}:{}/container/{}/logs/compact'.format(
        cont_json['node_ip'],
        cont_json['node_port'],
        cont_json['container_id']))

    return jsonify(request_json.json())


@app.route('/service/<string:name>/tasks/<string:id>/logs/stream')
def get_logs_by_task_id_stream(name, id):
    cont_json = get_container_by_task_id(name, id)

    if cont_json is None:
        abort(404)

    request_stream = requests.get('http://{}:{}/container/{}/logs/stream'.format(
        cont_json['node_ip'],
        cont_json['node_port'],
        cont_json['container_id']),
        stream=True)

    def generate_from_provider():
        for line in request_stream.iter_lines(chunk_size=1, decode_unicode=True):
            # yield str(line).strip() + '\n'
            yield line + '\n'

    return Response(generate_from_provider(), mimetype='text/plain')


@app.route('/service/<string:name>/tasks/<string:id>/logs/tail/<int:lines>')
def get_logs_by_task_id_stream_tail(name, id, lines):

    cont_json = get_container_by_task_id(name, id)

    if cont_json is None:
        abort(404)

    request_stream = requests.get('http://{}:{}/container/{}/logs/tail/{}'.format(
        cont_json['node_ip'],
        cont_json['node_port'],
        cont_json['container_id'],
        lines),
        stream=True)

    def generate_from_provider():
        for line in request_stream.iter_lines(chunk_size=1, decode_unicode=True):
            # yield str(line).strip() + '\n'
            yield line + '\n'

    return Response(generate_from_provider(), mimetype='text/plain')


@app.route('/service/<string:name>/logs/stream')
def get_service_logs(name):

    client = docker.APIClient(base_url='unix://var/run/docker.sock', version='auto')

    return Response(
        client.service_logs(
            name,
            details=False,
            timestamps=True,
            stdout=True,
            stderr=True,
            follow=True
        ), mimetype='text/plain')


@app.route('/service/<string:name>/logs/tail/<int:lines>')
def get_service_logs_tail(name, lines):

    client = docker.APIClient(base_url='unix://var/run/docker.sock', version='auto')

    return Response(
        client.service_logs(
            name,
            details=False,
            timestamps=True,
            stdout=True,
            stderr=True,
            follow=True,
            tail=lines
        ), mimetype='text/plain')


@app.route('/node')
def get_nodes_hostnames():
    return jsonify(get_node_json())


@app.route('/node/current')
def get_current_node():
    return jsonify(get_current_nodename())


if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=5000, use_evalex=False, threaded=True)
    # socketio.run(app,  host='0.0.0.0', port=5000, debug=False)
