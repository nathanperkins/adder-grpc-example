import logging
import os
import sys

import grpc

import adder_pb2
import adder_pb2_grpc

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("adder-client")

_ENDPOINT = os.environ.get("ENDPOINT")
_SECURE = os.environ.get("SECURE")
_VALUE = os.environ.get("VALUE")

if __name__ == '__main__':
    if not _ENDPOINT:
        logger.error(f"Need to provide ENDPOINT env var")
        sys.exit(1)

    if not _VALUE:
        logger.error(f"Need to provide VALUE env var")
        sys.exit(1)

    try:
        value = int(_VALUE)
    except Exception as err:
        logger.error(f"VALUE must be parseable as int: {err}")
        sys.exit(1)

    if _SECURE and _SECURE.upper() == "TRUE":
        logger.info(f"Using secure channel to {_ENDPOINT}")
        channel = grpc.secure_channel(_ENDPOINT, grpc.ssl_channel_credentials())
    else:
        logger.info(f"Using insecure channel to {_ENDPOINT}")
        channel = grpc.insecure_channel(_ENDPOINT)

    try:
        stub = adder_pb2_grpc.AdderStub(channel)
        req = adder_pb2.AddOneRequest(value=value)
        res = stub.AddOne(req)
        logger.info(f"Adding 1 to {value} = {res.value}")
    except Exception as err:
        logger.error(f"AddOne failed: {err}")
        sys.exit(1)
