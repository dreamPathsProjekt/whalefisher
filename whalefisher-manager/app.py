from flask import Flask
from flask import jsonify
from flask import Response
from flask import make_response
from flask import abort

from docker import client
import json

from flask_socketio import SocketIO
import eventlet
import requests

from docker_provider import *


eventlet.monkey_patch()
app = Flask(__name__)
# Redirect with or without slashes
app.url_map.strict_slashes = False

socketio = SocketIO(app, async_mode='eventlet')


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


@app.route('/error')
def test_error_handler():
    return abort(404)


# Commented for security reasons
# @app.route('/client')
# def get_client_info_route():
#     return jsonify(get_client_info())


@app.route('/service')
def get_services_route():
    return jsonify(get_service_json())


@app.route('/service/<string:name>')
def get_services_by_service_name(name):

    services = get_service_json_by_name(name)

    if len(services) == 0:
        abort(404)

    return jsonify(services)


# Requires exact name
@app.route('/service/<string:name>/tasks')
def get_tasks_by_service_name(name):

    tasks = get_tasks_json(tasks=get_running_tasks(name), service_name_input=name)

    if len(tasks) == 0:
        abort(404)

    return jsonify(tasks)


@app.route('/service/<string:name>/tasks/<string:id>')
def get_tasks_by_id(name, id):

    tasks = get_tasks_json(tasks=get_running_tasks(name, task_id=id), service_name_input=name)

    if len(tasks) == 0:
        abort(404)

    if len(tasks) > 1:
        return jsonify({'message': 'Multiple Tasks Found'})

    return jsonify(tasks[0])


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
        for line in request_stream.iter_lines(chunk_size=2048, decode_unicode=True):
            yield str(line).strip() + '\n'

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
        for line in request_stream.iter_lines(chunk_size=256, decode_unicode=True):
            yield str(line).strip() + '\n'

    return Response(generate_from_provider(), mimetype='text/plain')


@app.route('/node')
def get_nodes_hostnames():
    return jsonify(get_node_json())


@app.route('/node/current')
def get_current_node():
    return jsonify(get_current_nodename())


@app.route('/teststream')
def test_streaming_logs():
    # Below to be handled by middleware module
    req_get_name = requests.get('http://10.132.0.28:8086/container')

    cont_id = ''
    for container in req_get_name.json():
        if str(container['name']).startswith('ifg_logstash'):
            cont_id = container['id']

    request_stream = requests.get('http://10.132.0.28:8086/container/{}/logs/tail/20'.format(cont_id), stream=True)

    # for line in request_stream.iter_content(chunk_size=2048, decode_unicode=True):
    #     print(line)
    def generate_from_provider():
        for line in request_stream.iter_lines(chunk_size=2048, decode_unicode=True):
            yield str(line).strip() + '\n'

    return Response(generate_from_provider(), mimetype='text/plain')


if __name__ == "__main__":
    # app.run(debug=True, host='0.0.0.0', port=5000, use_evalex=False, threaded=False)
    socketio.run(app,  host='0.0.0.0', port=5000, debug=False)
