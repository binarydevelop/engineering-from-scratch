# ==============================================================================
# kafka-from-scratch Makefile
#
# IMPORTANT PEDAGOGICAL PRINCIPLE:
# Make != Docker != Kafka
#
# These targets are convenience shortcuts for laboratory workflows.
# Never rely on them blindly without understanding the underlying commands
# printed in each recipe.
# ==============================================================================

.PHONY: help env-check up up-cluster down logs logs-cluster reset-lab test clean topics cluster-info

help:
	@echo "kafka-from-scratch - Laboratory Automation"
	@echo "=========================================="
	@echo "Convenience targets (see Makefile for underlying commands):"
	@echo "  make env-check    : Run environment and dependency preflight check"
	@echo "  make up           : Launch single-broker KRaft Kafka container (ports 9092, 9093)"
	@echo "  make up-cluster   : Launch 3-broker KRaft cluster (ports 9092, 9094, 9096)"
	@echo "  make down         : Stop all running Kafka containers"
	@echo "  make logs         : Follow logs from single-broker Kafka container"
	@echo "  make logs-cluster : Follow logs from 3-broker cluster containers"
	@echo "  make reset-lab    : WIPE ALL volumes, partition logs, and reset environment"
	@echo "  make topics       : List all topics on the active Kafka broker"
	@echo "  make cluster-info : Describe cluster metadata using kafka-metadata-shell/cluster tool"
	@echo "  make test         : Run automated curriculum verification test suite"
	@echo "  make clean        : Remove Python caches and temporary test dumps"

env-check:
	@echo "--> Executing: ./scripts/check-environment.sh"
	@./scripts/check-environment.sh

up:
	@echo "--> Executing: ./scripts/start-kafka.sh single"
	@./scripts/start-kafka.sh single

up-cluster:
	@echo "--> Executing: ./scripts/start-kafka.sh cluster"
	@./scripts/start-kafka.sh cluster

down:
	@echo "--> Executing: ./scripts/stop-kafka.sh"
	@./scripts/stop-kafka.sh

logs:
	@echo "--> Executing: docker compose logs -f kafka"
	docker compose logs -f kafka

logs-cluster:
	@echo "--> Executing: docker compose -f docker-compose.cluster.yml logs -f"
	docker compose -f docker-compose.cluster.yml logs -f

topics:
	@echo "--> Executing: docker exec -it kafka-lab-single /opt/kafka/bin/kafka-topics.sh --bootstrap-server localhost:9092 --list"
	@docker exec kafka-lab-single /opt/kafka/bin/kafka-topics.sh --bootstrap-server localhost:9092 --list 2>/dev/null || docker exec kafka-node-1 /opt/kafka/bin/kafka-topics.sh --bootstrap-server localhost:9092 --list

cluster-info:
	@echo "--> Executing: docker exec kafka-lab-single /opt/kafka/bin/kafka-cluster.sh cluster-id --bootstrap-server localhost:9092"
	@docker exec kafka-lab-single /opt/kafka/bin/kafka-cluster.sh cluster-id --bootstrap-server localhost:9092 2>/dev/null || docker exec kafka-node-1 /opt/kafka/bin/kafka-cluster.sh cluster-id --bootstrap-server localhost:9092

reset-lab:
	@echo "--> Executing: ./scripts/reset-lab.sh"
	@./scripts/reset-lab.sh

test:
	@echo "--> Executing curriculum verification tests..."
	./.venv/bin/pytest tests/ -v || ./.venv/bin/python3 scripts/run-all-tests.py

clean:
	@echo "--> Cleaning bytecode, caches, and test artifacts..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	rm -rf outputs/*.log outputs/*.bin
