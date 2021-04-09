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

1. Start flask socketIO server.

2. Open two page with url `http://localhost:8001/index` (one Chrome, and another Safari).

3. Input message and submit, and both pages will show the submitted message.

Workflow:

1. login
  - server route `/index`
  - client on connect event -> emit login event
  - server on login event -> emit login event
  - client on login event -> print

2. submit
  - server route `/listen` -> emit msg event
  - client on msg event -> show message

