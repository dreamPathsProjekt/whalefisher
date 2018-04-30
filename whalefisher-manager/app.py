from flask import Flask
from flask import jsonify
from flask import Response
from flask import make_response
from flask import abort

from docker import client
import json

from flask_socketio import SocketIO
import eventlet

from docker_provider import *


app = Flask(__name__)
# Redirect with or without slashes
app.url_map.strict_slashes = False

eventlet.monkey_patch()
socketio = SocketIO(app)


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


@app.route('/node')
def get_nodes_hostnames():
    return jsonify(get_node_json())


@app.route('/node/current')
def get_current_node():
    return jsonify(get_current_nodename())


@app.route('/container')
def containers_route():
    return jsonify(get_container_json())


@app.route('/logs')
def get_logs():
    containers = get_containers()[2]

    logs = str(containers.logs(timestamps=True, stream=False), encoding='utf-8').split('\n')

    # def generate_stream(logs):
    #     for log in logs:
    #         yield str(log, 'utf-8').strip() + '\n'
    lines = []
    key = 0
    for log in logs:
        log_json = {
            "Name": containers.name,
            "Line {}".format(key): log
        }
        lines.append(log_json)
        key += 1

    containers.reload()

    return jsonify(lines)


@app.route('/logs/compact')
def get_logs_compact():
    containers = get_containers()[1]
    logs = str(containers.logs(timestamps=True, stream=False), encoding='utf-8').split('\n')

    return jsonify(logs)

if __name__ == "__main__":
    # app.run(debug=True, host='0.0.0.0', port=5000, use_evalex=False, threaded=False)
    socketio.run(app,  host='0.0.0.0', port=5000, debug=False)
