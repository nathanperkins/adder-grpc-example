PYTHON=python3

GENERATED= \
	adder_pb2.py \
	adder_pb2_grpc.py

.PHONY: run-server
run-server: server.py $(GENERATED)
	python3 $<

.PHONY: run-client
run-client: client.py $(GENERATED)
	python3 $< 20

$(GENERATED): adder.proto
	$(PYTHON) -m grpc_tools.protoc -I=. --python_out=. --grpc_python_out=. $^
