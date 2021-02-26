from concurrent import futures
import logging
import os
import sys

import grpc

import adder_pb2
import adder_pb2_grpc

def add_one(val):
    return val + 1

class AdderServicer(adder_pb2_grpc.AdderServicer):
    def AddOne(self, request, context):
        val = request.value
        ret = add_one(val)
        print(f"Server: adding 1 to {val} = {ret}")
        return adder_pb2.AddOneResponse(value=ret)

def serve(port):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    adder_pb2_grpc.add_AdderServicer_to_server(
        AdderServicer(), server)
    server.add_insecure_port(f"[::]:{port}")
    server.start()
    print("Server starting.", flush=True)
    server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig()
    port = os.environ.get('PORT')
    if not port:
        print("PORT must be provided by env var", file=sys.stderr)
        sys.exit(1)

    serve(port)
