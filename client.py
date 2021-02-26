import logging
import sys

import grpc

import adder_pb2
import adder_pb2_grpc

if __name__ == '__main__':
    logging.basicConfig()
    if len(sys.argv) < 2:
        print(f"usage: {sys.argv[0]} value", file=sys.stderr)
        sys.exit(1)

    try:
        value = int(sys.argv[1])
    except Exception as err:
        print(f"failed to convert {sys.argv[1]} to int: {err}",
            file=sys.stderr)
        sys.exit(1)

    with grpc.insecure_channel('localhost:5000') as channel:
        stub = adder_pb2_grpc.AdderStub(channel)
        req = adder_pb2.AddOneRequest(value=value)
        res = stub.AddOne(req)
        print(f"Client: adding 1 to {value} = {res.value}")
