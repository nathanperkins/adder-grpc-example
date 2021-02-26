import logging
import os
import sys

import grpc

import adder_pb2
import adder_pb2_grpc

_ENDPOINT = os.environ.get("ENDPOINT")
_SECURE = os.environ.get("SECURE")
_VALUE = os.environ.get("VALUE")

if __name__ == '__main__':
    logging.basicConfig()

    if not _ENDPOINT:
        print(f"Error: need to provide ENDPOINT env var", file=sys.stderr)
        sys.exit(1)

    if not _VALUE:
        print(f"Error: need to provide VALUE env var", file=sys.stderr)
        sys.exit(1)

    try:
        value = int(_VALUE)
    except Exception as err:
        print(f"Error: value must be parseable as int: {err}", file=sys.stderr)
        sys.exit(1)

    if _SECURE and _SECURE.upper() == "TRUE":
        print(f"Using secure channel to {_ENDPOINT}")
        channel = grpc.secure_channel(_ENDPOINT, grpc.ssl_channel_credentials())
    else:
        print(f"Using insecure channel to {_ENDPOINT}")
        channel = grpc.insecure_channel(_ENDPOINT)

    try:
        stub = adder_pb2_grpc.AdderStub(channel)
        req = adder_pb2.AddOneRequest(value=value)
        res = stub.AddOne(req)
        print(f"Client: adding 1 to {value} = {res.value}")
    except Exception as err:
        print(f"Client: AddOne failed: {err}", file=sys.stderr)
        sys.exit(1)
