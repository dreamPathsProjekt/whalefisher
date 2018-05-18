# WhaleFisher

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
![GitHub (pre-)release](https://img.shields.io/badge/pre--release-0.9.1-blue.svg)

A simple read-only Docker Swarm Logging Api, to export or stream logs to HTTP from containers across different nodes inside a Swarm.

- [WhaleFisher](#whalefisher)
    - [API v0.9 Documentation](#api-v09-documentation)
        - [Client-Browser Guidelines](#client-browser-guidelines)
        - [Services](#services)
        - [Service Logs and Container Logs](#service-logs-and-container-logs)
            - [Container/Task Logs](#container-task-logs)
            - [Service Logs](#service-logs)
        - [General Notes](#general-notes)
        - [Low Level Container Api](#low-level-container-api)
    - [Future Additions - TODO](#future-additions---todo)

## API v0.9 Documentation

### Client-Browser Guidelines

- It is advised to use __Chrome, Firefox__ or __Edge__ with a __Json Formatter__ extension (e.g. Chrome Ext: `JSON Formatter`), for your own links-navigation convenience.
- You can also use REST clients like __Postman__ for JSON Endpoints but live __streaming log routes do not work__.
- Cli tools like __curl__ also work with both JSON and Streaming Routes.

### Services

- `/`: List All Routes
- `/service/`: List All Swarm Services
- `/service/<string:name>`: Search Swarm Services
  - Example: `http://35.189.200.49/service/whale` returns a list of json service obj where name contains string `whale`
  - Output:

```JSON
[
    {
        "_links": {
            "_self": "http://35.189.200.49:80/service/whale_whalefisher-data_provider",
            "logs": {
                "stream": "http://35.189.200.49:80/service/whale_whalefisher-data_provider/logs/stream"
            },
            "tasks": "http://35.189.200.49:80/service/whale_whalefisher-data_provider/tasks"
        },
        "id": "bazngvc41saozxqwnb80p92ip",
        "name": "whale_whalefisher-data_provider"
    },
    {
        "_links": {
            "_self": "http://35.189.200.49:80/service/whale_whalefisher-manager",
            "logs": {
                "stream": "http://35.189.200.49:80/service/whale_whalefisher-manager/logs/stream"
            },
            "tasks": "http://35.189.200.49:80/service/whale_whalefisher-manager/tasks"
        },
        "id": "tww67edxg3duq644e007vx0jn",
        "name": "whale_whalefisher-manager"
    }
]
```

- `/service/<string:exact_name>/tasks`: If exact service name is used, `/tasks/` returns a list of docker swarm tasks running for that service. E.g. if a service with name `elastic_elasticsearch` has 3 running replicas, `/tasks` should return a list of those replicas. For convenience use the pseudo-HATEOAS link: `tasks` under `_links`

- `/service/<string:exact_name>/tasks/<string:task_id>`: Returns the exact running task with the specified id. You can also use truncated ids, as in the below example:
- - `http://35.189.200.49/service/elastic_elasticsearch/tasks/kad1` In the output you can see the full task id used for the request:

```JSON
{
    "_links": {
        "_self": "http://35.189.200.49:80/service/elastic_elasticsearch/tasks/kad1nusozo8089egzn4hwudud",
        "logs": {
            "compact": "http://35.189.200.49:80/service/elastic_elasticsearch/tasks/kad1nusozo8089egzn4hwudud/logs/compact",
            "json": "http://35.189.200.49:80/service/elastic_elasticsearch/tasks/kad1nusozo8089egzn4hwudud/logs",
            "stream": "http://35.189.200.49:80/service/elastic_elasticsearch/tasks/kad1nusozo8089egzn4hwudud/logs/stream"
        },
        "service": "http://35.189.200.49:80/service/elastic_elasticsearch"
    },
    "current_state": "running",
    "desired_state": "running",
    "id": "kad1nusozo8089egzn4hwudud",
    "node_id": "lue9l1amt3x1v0xbputcops7f",
    "node_name": "dream-paths",
    "service_id": "r8iyt20mqn65gedc2sk6iz78a",
    "service_name": "elastic_elasticsearch",
    "slot": null
}
```

- `_links: {logs: }` field on `/tasks/...` redirect to container/task log output
- `_links: {logs: }` field on `/services/...` redirect to swarm service logs (contain service level logs from all tasks)
- Below you can find details about different log viewing options

### Service Logs and Container Logs

#### Container/Task Logs

- `/service/<string:exact_name>/tasks/<string:task_id>/logs/` returns a list of __container__ log lines with timestamp and container names.
- - Example request: `http://35.189.200.49/service/elastic_elasticsearch/tasks/kad1nusozo8089egzn4hwudud/logs`

```JSON
// ...
[{
    "Line 398": "2018-05-18T00:44:12.972502668Z \tat java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:624)",
    "Name": "elastic_elasticsearch.lue9l1amt3x1v0xbputcops7f.kad1nusozo8089egzn4hwudud",
    "Timestamp": "2018-05-18T00:44:12.972502668"
}, {
    "Line 399": "2018-05-18T00:44:12.972505198Z \tat java.lang.Thread.run(Thread.java:748)",
    "Name": "elastic_elasticsearch.lue9l1amt3x1v0xbputcops7f.kad1nusozo8089egzn4hwudud",
    "Timestamp": "2018-05-18T00:44:12.972505198"
}, {
    "Line 400": "",
    "Name": "elastic_elasticsearch.lue9l1amt3x1v0xbputcops7f.kad1nusozo8089egzn4hwudud",
    "Timestamp": ""
}]
// ...
```

- `/service/<string:exact_name>/tasks/<string:task_id>/logs/compact/` returns a list of JSONified strings, example output:

```JSON
[
    "2018-05-01T17:35:29.786470420Z [2018-05-01 17:35:29,785][WARN ][bootstrap                ] unable to install syscall filter: seccomp unavailable: your kernel is buggy and you should upgrade",
    "2018-05-01T17:35:30.179505631Z [2018-05-01 17:35:30,179][INFO ][node                     ] [Huntara] version[2.4.6], pid[1], build[5376dca/2017-07-18T12:17:44Z]",
    "2018-05-01T17:35:30.179796393Z [2018-05-01 17:35:30,179][INFO ][node                     ] [Huntara] initializing ...",
    "2018-05-01T17:35:31.201964187Z [2018-05-01 17:35:31,201][INFO ][plugins                  ] [Huntara] modules [reindex, lang-expression, lang-groovy], plugins [], sites []",
    "2018-05-01T17:35:31.310685060Z [2018-05-01 17:35:31,310][INFO ][env                      ] [Huntara] using [1] data paths, mounts [[/usr/share/elasticsearch/data (/dev/sda1)]], net usable_space [4.5gb], net total_space [9.6gb], spins? [possibly], types [ext4]",
    "2018-05-01T17:35:31.310906578Z [2018-05-01 17:35:31,310][INFO ][env                      ] [Huntara] heap size [1015.6mb], compressed ordinary object pointers [true]",
    "2018-05-01T17:35:34.455737006Z [2018-05-01 17:35:34,455][INFO ][node                     ] [Huntara] initialized",
    "2018-05-01T17:35:34.461570654Z [2018-05-01 17:35:34,461][INFO ][node                     ] [Huntara] starting ...",
    "2018-05-01T17:35:34.618512332Z [2018-05-01 17:35:34,618][INFO ][transport                ] [Huntara] publish_address {10.0.3.3:9300}, bound_addresses {0.0.0.0:9300}",
    "2018-05-01T17:35:34.624375994Z [2018-05-01 17:35:34,624][INFO ][discovery                ] [Huntara] elasticsearch/Yx7UjAdZT7q0iOLz82IyTg",
    "2018-05-01T17:36:04.627214323Z [2018-05-01 17:36:04,626][WARN ][discovery                ] [Huntara] waited for 30s and no initial state was set by the discovery",
    "2018-05-01T17:36:04.640998255Z [2018-05-01 17:36:04,640][INFO ][http                     ] [Huntara] publish_address {10.0.3.3:9200}, bound_addresses {0.0.0.0:9200}",
    "2018-05-01T17:36:04.647201506Z [2018-05-01 17:36:04,647][INFO ][node                     ] [Huntara] started",
    "2018-05-02T17:09:45.701716652Z [2018-05-02 17:09:45,695][DEBUG][action.admin.indices.get ] [Huntara] no known master node, scheduling a retry",
    "2018-05-02T17:09:56.235000314Z [2018-05-02 17:09:56,216][WARN ][rest.suppressed          ] path: /_stats, params: {}",
    "2018-05-02T17:09:56.235020569Z ClusterBlockException[blocked by: [SERVICE_UNAVAILABLE/1/state not recovered / initialized];]",
    "2018-05-02T17:09:56.235024660Z \tat org.elasticsearch.cluster.block.ClusterBlocks.globalBlockedException(ClusterBlocks.java:158)",
    "2018-05-02T17:09:56.235028274Z \tat org.elasticsearch.action.admin.indices.stats.TransportIndicesStatsAction.checkGlobalBlock(TransportIndicesStatsAction.java:70)",
    "2018-05-02T17:09:56.235031773Z \tat org.elasticsearch.action.admin.indices.stats.TransportIndicesStatsAction.checkGlobalBlock(TransportIndicesStatsAction.java:47)",
    "2018-05-02T17:09:56.235034823Z \tat org.elasticsearch.action.support.broadcast.node.TransportBroadcastByNodeAction$AsyncAction.<init>(TransportBroadcastByNodeAction.java:260)",
    "2018-05-02T17:09:56.235038068Z \tat org.elasticsearch.action.support.broadcast.node.TransportBroadcastByNodeAction.doExecute(TransportBroadcastByNodeAction.java:238)",
    "2018-05-02T17:09:56.235040992Z \tat org.elasticsearch.action.support.broadcast.node.TransportBroadcastByNodeAction.doExecute(TransportBroadcastByNodeAction.java:79)",
    "2018-05-02T17:09:56.235069404Z \tat org.elasticsearch.action.support.TransportAction.execute(TransportAction.java:137)",
    "2018-05-02T17:09:56.235073838Z \tat org.elasticsearch.action.support.TransportAction.execute(TransportAction.java:85)",
    "2018-05-02T17:09:56.235076466Z \tat org.elasticsearch.client.node.NodeClient.doExecute(NodeClient.java:58)",
    "2018-05-02T17:09:56.235078975Z \tat org.elasticsearch.client.support.AbstractClient.execute(AbstractClient.java:359)",
]
```

- __Important:__ Very large log output, when requested as a single response, may grow substantially large (you can view network tab in developer tools as it loads). For those use-cases, it is best advised to use streaming endpoints as described below.

- `/service/<string:exact_name>/tasks/<string:task_id>/logs/stream/` returns a __plain-text__ stream of logs from the creation of a container till now.
- - CLI tools like curl also retain terminal-color settings from the initial logs.

- `/service/<string:exact_name>/tasks/<string:task_id>/logs/tail/<int:lines>` returns the tail of last `lines` log lines till now, with `lines` provided in the url. Additional realtime output is appended.
- - Example request: `http://35.189.200.49/service/elastic_elasticsearch/tasks/kad1nusozo8089egzn4hwudud/logs/tail/10`

- - Output:

```Shell
2018-05-18T00:44:12.972480658Z 	at org.jboss.netty.channel.socket.nio.NioWorker.read(NioWorker.java:88)
2018-05-18T00:44:12.972483231Z 	at org.jboss.netty.channel.socket.nio.AbstractNioWorker.process(AbstractNioWorker.java:108)
2018-05-18T00:44:12.972485755Z 	at org.jboss.netty.channel.socket.nio.AbstractNioSelector.run(AbstractNioSelector.java:337)
2018-05-18T00:44:12.972488454Z 	at org.jboss.netty.channel.socket.nio.AbstractNioWorker.run(AbstractNioWorker.java:89)
2018-05-18T00:44:12.972492366Z 	at org.jboss.netty.channel.socket.nio.NioWorker.run(NioWorker.java:178)
2018-05-18T00:44:12.972494958Z 	at org.jboss.netty.util.ThreadRenamingRunnable.run(ThreadRenamingRunnable.java:108)
2018-05-18T00:44:12.972497471Z 	at org.jboss.netty.util.internal.DeadLockProofWorker$1.run(DeadLockProofWorker.java:42)
2018-05-18T00:44:12.972500133Z 	at java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1149)
2018-05-18T00:44:12.972502668Z 	at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:624)
2018-05-18T00:44:12.972505198Z 	at java.lang.Thread.run(Thread.java:748)
```

- __Important:__ Streamed/Tail Responses load faster than JSON Responses but keep the connection alive forever, as they follow log output in real-time. For small log outputs it is usually faster to use the JSON Routes

#### Service Logs

Service-Level logs can be only viewed as streamed Responses, due to limitations in the Docker Low-Level Api. Keep in mind that individual container logs may be included mixed in service-level logs, as they are asynchronously updated when individual Docker tasks are started and finished.

- `/service/<string:exact_name>/logs/stream` returns a __plain-text__ stream of logs.
- `/service/<string:exact_name>/logs/tail/<int:lines>` returns the tail of last `lines` service-log lines till now, with `lines` provided in the url. Additional realtime output is appended.

### General Notes

- For your own convenience you can navigate the Api using the pseudo-HATEOAS `_links` objects.
- When a URI resource is not found, the output produced is:

```JSON
{
    "error": "Not found"
}
```

- - The above response may occur on wrong input, or during a Docker Service is restarting individual containers. At this situation __individual task ids are recreated__, so it is advised to refresh the `.../tasks/` endpoint and follow the new recreated ids.

- - It is not recommended to use values <= 5 on `/tail/lines` routes. As of newer versions of the API (0.9 and later), fewer than 5 lines return a `400 error - bad request`

```JSON
{
    "error": "Bad Request"
}
```

### Low Level Container Api

It is generally not advisable to view logs using the low-level Api.

If you, however, wish to view individual containers on each host via the data provider global service, you can use the data provider's host ip with it's exported port:

- `/node/current`: Returns the hostname of the individual node you are sending requests to.
- - Example Request: `http://35.189.200.49:8080/node/current`
- - Output:

```JSON
{
    "current": "dream-paths"
}
```

- `/container/<string:id>`: Returns an individual container's info. Container ids can be also submitted truncated.
- The Below URIs work according to the High-Level Api Template, as documented earlier:
- - `/container/<string:id>/logs/`
- - `/container/<string:id>/logs/compact/`
- - `/container/<string:id>/logs/stream/`
- - `/container/<string:id>/logs/tail/<int:lines>`

## Future Additions - TODO

- Include Authorization
- Implement `since` & `until` routes to find logs within a given timeframe.