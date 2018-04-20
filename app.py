from flask import Flask
from docker import client

from test import get_container_json, get_containers

docker_client = client.from_env()
app = Flask(__name__)


@app.route('/')
def welcome():
    return 'Welcome to Whalefisher Logging Api!'


@app.route('/containers')
def containers_route():
    return get_container_json(docker_client)


@app.route('/logs')
def get_logs():
    containers = get_containers(docker_client)[2]
    logs = containers.logs(stream=True)

    return [str(log, 'utf-8').strip() for log in logs]


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000, use_evalex=False)