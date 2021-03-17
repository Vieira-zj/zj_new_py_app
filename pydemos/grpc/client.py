import grpc
import helloworld_pb2
import helloworld_pb2_grpc

HOST = 'localhost'
PORT = '50051'


def main():
    # pre-condition: start grpc server from "zj_go2_project/demo.hello/grpc"
    with grpc.insecure_channel(f'{HOST}:{PORT}') as channel:
        client = helloworld_pb2_grpc.GreeterStub(channel=channel)
        response = client.SayHello(helloworld_pb2.HelloRequest(name='test'))
        print('received: ', response.message)


if __name__ == '__main__':
    main()
