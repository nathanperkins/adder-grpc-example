from concurrent import futures
import logging
import os
import sys

import grpc

import adder_pb2
import adder_pb2_grpc

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(name="adder-server")

def add_one(val):
    return val + 1

class AdderServicer(adder_pb2_grpc.AdderServicer):
    def AddOne(self, request, context):
        val = request.value
        ret = add_one(val)
        logger.info(f"Adding 1 to {val} = {ret}")
        return adder_pb2.AddOneResponse(value=ret)

def serve(port):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    adder_pb2_grpc.add_AdderServicer_to_server(
        AdderServicer(), server)
    server.add_insecure_port(f"[::]:{port}")
    server.start()
    logger.info("Starting.")
    server.wait_for_termination()

if __name__ == '__main__':
    port = os.environ.get('PORT')
    if not port:
        logger.error("PORT must be provided by env var")
        sys.exit(1)

    serve(port)
