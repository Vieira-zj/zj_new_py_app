# Flask Socket IO Demo

> A flash socketIO demo.

## Condition

1. Install socketIO

```sh
pip3 install flask-socketio
```

2. Start a redis for session

```sh
docker run --name redis --rm -d -p 6379:6379 redis
```

## Run and Test

1. Start flask socketIO server

2. Open page `http://localhost:8001/index`

Workflow:

1. login
  - server route `/index`
  - client on connect event -> emit login event
  - server on login event -> emit login event
  - client on login event

2. submit
  - server route `/listen` -> emit msg event
  - client on msg event -> show message

