from concurrent import futures
import logging

import grpc

import adder_pb2
import adder_pb2_grpc

def add_one(val):
    return val + 1

class AdderServicer(adder_pb2_grpc.AdderServicer):
    def AddOne(self, request, context):
        val = request.value
        ret = add_one(request.value)
        print(f"adding 1 to {val}: {ret}")
        return adder_pb2.AddOneResponse(value=ret)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    adder_pb2_grpc.add_AdderServicer_to_server(
        AdderServicer(), server)
    server.add_insecure_port('[::]:5000')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig()
    serve()
