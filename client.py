import logging
import sys

import grpc

import adder_pb2
import adder_pb2_grpc

if __name__ == '__main__':
    logging.basicConfig()
    if len(sys.argv) < 2:
        print(f"usage: {sys.argv[0]} value")
        sys.exit(1)

    value = int(sys.argv[1])

    with grpc.insecure_channel('localhost:5000') as channel:
        stub = adder_pb2_grpc.AdderStub(channel)
        req = adder_pb2.AddOneRequest(value=value)
        res = stub.AddOne(req)
        print(f"result of adding 1 to {value}: {res.value}")
