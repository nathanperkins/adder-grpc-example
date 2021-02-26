import logging
import os
import sys

import grpc

import adder_pb2
import adder_pb2_grpc

_SECURE = os.environ.get("SECURE")

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

    if _SECURE and _SECURE.upper() == "TRUE":
        print("Using secure channel")
        channel = grpc.secure_channel(endpoint, grpc.ssl_channel_credentials())
    else:
        print("Using insecure channel")
        channel = grpc.insecure_channel(endpoint)

    try:
        stub = adder_pb2_grpc.AdderStub(channel)
        req = adder_pb2.AddOneRequest(value=value)
        res = stub.AddOne(req)
        print(f"Client: adding 1 to {value} = {res.value}")
    except Exception as err:
        print(f"Failed to AddOne: {err}", file=sys.stderr)
        sys.exit(1)
