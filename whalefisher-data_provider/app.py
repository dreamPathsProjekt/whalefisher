from flask import Flask
from flask import jsonify
from flask import Response
from flask import make_response
from flask import abort
from flask import stream_with_context


from flask_socketio import SocketIO
import eventlet

from docker import client
import json
import time

from docker_provider import *

# The init_app() style of initialization is also supported. Note the way the web server is started.
# The socketio.run() function encapsulates the start up of the web server and replaces the app.run() standard Flask development server start up.
# When the application is in debug mode the Werkzeug development server is still used and configured properly inside socketio.run().
# In production mode the eventlet web server is used if available, else the gevent web server is used.
# If eventlet and gevent are not installed, the Werkzeug development web server is used.

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

    # container.reload()

    return jsonify(lines)


@app.route('/container/<string:id>/logs/compact')
def get_logs_compact(id):
    container = get_container_by_id(id)
    logs = str(container.logs(timestamps=True, stream=False), encoding='utf-8').split('\n')

    return jsonify(logs)


@app.route('/container/<string:id>/logs/stream')
def get_logs_stream(id):
    container = get_container_by_id(id)

    # @stream_with_context
    def generate_stream():
        try:
            logs = container.logs(timestamps=True, stream=True, follow=True)
            # while True:
            #     # yield str(log, 'utf-8').strip() + '\n'
            #     yield logs.next()
            #     # container.reload()
            yield from logs
        except docker.errors.APIError:
            yield 'Error from Docker Api\n'

    return app.response_class(generate_stream(),  mimetype='text/event-stream')


@app.route('/container/<string:id>/logs/tail/<int:lines>')
def get_logs_stream_tail(id, lines):
    container = get_container_by_id(id)

    # @stream_with_context
    def generate_tail():
        try:
            logs = container.logs(timestamps=True, stream=True, tail=lines, follow=True)
            # for log in container.logs(timestamps=True, stream=True, tail=lines, follow=True):
            #     # yield str(log, 'utf-8').strip() + '\n'
            #     yield log
            #     # container.reload()
            yield from logs
        except docker.errors.APIError:
            yield 'Error from Docker Api\n'

    return app.response_class(generate_tail(),  mimetype='text/event-stream')


if __name__ == "__main__":
    # app.run(debug=False, host='0.0.0.0', port=5000, use_evalex=False, threaded=True)
    socketio.run(app,  host='0.0.0.0', port=5000, debug=False)
