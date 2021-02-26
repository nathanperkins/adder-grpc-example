PYTHON=python3
VALUE=20

GENERATED= \
	adder_pb2.py \
	adder_pb2_grpc.py

.PHONY: run-server
run-server: server.py $(GENERATED)
	$(PYTHON) $<

.PHONY: run-client
run-client: client.py $(GENERATED)
	$(PYTHON) $< $(VALUE)

$(GENERATED): adder.proto
	$(PYTHON) -m grpc_tools.protoc -I=. --python_out=. --grpc_python_out=. $^
