from flask import Flask
from flask import jsonify
from flask import Response

from docker import client
import json

from test import get_container_json, get_containers

docker_client = client.from_env()
app = Flask(__name__)


@app.route('/')
def welcome():
    return 'Welcome to Whalefisher Logging Api!'


@app.route('/containers')
def containers_route():
    return jsonify(get_container_json(docker_client))


@app.route('/logs')
def get_logs():
    containers = get_containers(docker_client)[0]
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

    return jsonify(lines)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000, use_evalex=False)