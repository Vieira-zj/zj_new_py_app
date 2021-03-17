#!/bin/bash
set -x

python -m grpc_tools.protoc -I ./ --python_out=./ --grpc_python_out=./ helloworld.proto
echo "done"