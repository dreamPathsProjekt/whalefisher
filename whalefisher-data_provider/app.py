from flask import Flask
from flask import jsonify
from flask import Response
from flask import make_response
from flask import abort

from docker import client
import json

from docker_provider import *


app = Flask(__name__)
# Redirect with or without slashes
app.url_map.strict_slashes = False


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


@app.route('/node/current')
def get_current_node():
    return jsonify(get_current_nodename())


@app.route('/container')
def containers_route():
    return jsonify(get_container_json())


@app.route('/container/<string:id>')
def container_by_id(id):
    return jsonify(get_container_json_by_id(id))


@app.route('/container/<string:id>/logs')
def get_logs(id):
    container = get_container_by_id(id)

    logs = str(container.logs(timestamps=True, stream=False), encoding='utf-8').split('\n')

    # def generate_stream(logs):
    #     for log in logs:
    #         yield str(log, 'utf-8').strip() + '\n'
    lines = []
    key = 0
    for log in logs:
        log_json = {
            "Name": container.name,
            "Line {}".format(key): log
        }
        lines.append(log_json)
        key += 1

    container.reload()

    return jsonify(lines)


@app.route('/container/<string:id>/logs/compact')
def get_logs_compact(id):
    container = get_container_by_id(id)
    logs = str(container.logs(timestamps=True, stream=False), encoding='utf-8').split('\n')

    return jsonify(logs)


@app.route('/container/<string:id>/logs/stream')
def get_logs_stream(id):
    container = get_container_by_id(id, client)

    def generate_stream():
        for log in container.logs(timestamps=True, stream=True):
            yield str(log, 'utf-8').strip()
            container.reload()

    return Response(generate_stream(),  mimetype='text/plain')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000, use_evalex=False, threaded=False)