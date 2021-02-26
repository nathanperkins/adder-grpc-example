import logging
import sys

import grpc

import adder_pb2
import adder_pb2_grpc

if __name__ == '__main__':
    logging.basicConfig()
    if len(sys.argv) < 3:
        print(f"usage: {sys.argv[0]} server:port value", file=sys.stderr)
        sys.exit(1)
    
    endpoint = sys.argv[1]

    try:
        value = int(sys.argv[2])
    except Exception as err:
        print(f"failed to convert {sys.argv[2]} to int: {err}",
            file=sys.stderr)
        sys.exit(1)

    with grpc.insecure_channel(endpoint) as channel:
        stub = adder_pb2_grpc.AdderStub(channel)
        req = adder_pb2.AddOneRequest(value=value)
        res = stub.AddOne(req)
        print(f"Client: adding 1 to {value} = {res.value}")
