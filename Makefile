PYTHON=python3
VALUE=20
SERVER_TAG=adder-server
NETWORK=adder
PORT=5000
CLIENT_TAG=adder-client


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

.PHONY: docker-build
docker-build: $(GENERATED)
	docker build -f Dockerfile.server -t $(SERVER_TAG) .
	docker build -f Dockerfile.client -t $(CLIENT_TAG) .

.PHONY: docker-run-server
docker-run-server: docker-build docker-network
	docker run \
		--name adder-server \
		--rm \
		--network $(NETWORK) \
		--env PORT=$(PORT) \
		-p $(PORT):$(PORT) \
		$(SERVER_TAG)

.PHONY: docker-run-client
docker-run-client: docker-build docker-network
	docker run \
		--name adder-client \
		--rm \
		--network $(NETWORK) \
		--env ENDPOINT=$(SERVER_TAG):$(PORT) \
		--env VALUE=$(VALUE) \
		$(CLIENT_TAG)

.PHONY: docker-network
docker-network:
	docker network create $(NETWORK) 2>&1 | grep -v "already exists" || true
