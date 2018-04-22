from flask import Flask
from flask import jsonify
from flask import Response
from flask import make_response
from flask import abort

from docker import client
import json

from docker_provider import get_container_json, get_containers, get_services, get_nodes, get_node_json, get_client_info


app = Flask(__name__)
# Redirect with or without slashes
app.url_map.strict_slashes = False


@app.route('/')
def welcome():
    return 'Welcome to Whalefisher Logging Api!'


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


@app.route('/tasks')
def get_tasks():

    tasks = get_services()[1].tasks(filters={"desired-state": "running"})


    if len(tasks) == 0:
        abort(404)

    return jsonify(tasks)


@app.route('/nodes')
def get_nodes_hostnames():
    return jsonify(get_node_json())


@app.route('/containers')
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
    app.run(debug=True, host='0.0.0.0', port=5000, use_evalex=False)