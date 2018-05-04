# Changelog

## 0.6.0

## 0.5.0

- Added streaming requests (removed sockets), using `chunk size=1024`
- Added route tasks_by_id for manager
- Fixed Leader key not exists
- Implemented return container id from task id & service name
- Added routes for logs, /compact, /stream, /tail/:lines
- Cleaned up docker_provider
- Included data-provider port as environment variable `DATA_PROVIDER_PORT`
- Added version=auto on docker client
- Reverted to flask instead of eventlet-socketio as server

## 0.4.0

- Included install of eventlet, flask-socketio, socketIO_client on both manager and data-provider
- Added async mode (eventlet) on SocketIO init
- Introduced threaded=True server for manager

## 0.3.0-0.3.8

- __Breaking Change:__ Split into data-provider and manager services
- Added container/id/logs routes on data-provider
- Added stream log route to data-provider
- Added tail/lines route to data-provider
- Introduced threaded=True server for data-provider
- Implemented initial tests to stream from manager using `iter_lines()` and `iter_content()`
- Discovered data loss from stream=True request, bug in 0.3.8

## 0.2.6-0.2.8

- Added active node by getting environment variable `DOCKER_NODE`
- Fixed empty list bug in tasks
- Added fields to tasks, get node by id
- Fixed client decorator behaviour
- Added Slot Check for Global Services

## 0.2.0-0.2.6

- Included new setup versions
- Included node labels, availability
- Added Routes: service, tasks by service name, search services by name, list routes

## 0.1.0

- Added Filtering Tasks with `desired-state=running`
- Use Docker Client as Decorator
- Strict Slashes Urls=false
- Base Routes Added