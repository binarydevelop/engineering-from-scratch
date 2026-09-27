# ==============================================================================
# elasticsearch-from-scratch Makefile
#
# PEDAGOGICAL PRINCIPLE:
# Make != Docker != Elasticsearch
#
# These targets are convenience shortcuts for lab workflows.
# Never treat these targets as magic; always understand the underlying curl and
# docker commands printed in each recipe.
# ==============================================================================

.PHONY: help env-check up down cluster-up cluster-down reset-lab health test clean

help:
	@echo "elasticsearch-from-scratch - Laboratory Automation"
	@echo "=================================================="
	@echo "Core convenience targets:"
	@echo "  make env-check    : Verify Python, Docker, Docker Compose, curl, and network"
	@echo "  make up           : Launch single-node Elasticsearch lab (es-lab-01 on :9200)"
	@echo "  make down         : Stop all Elasticsearch containers"
	@echo "  make cluster-up   : Launch 3-node distributed Elasticsearch cluster lab"
	@echo "  make cluster-down : Stop 3-node distributed Elasticsearch cluster lab"
	@echo "  make health       : Display current cluster health and shard allocation"
	@echo "  make reset-lab    : Wipe user indices, reset blocks, and clear temp data"
	@echo "  make test         : Run automated validation test suite across all phases"
	@echo "  make clean        : Clean temporary caches, logs, and Python bytecode"

env-check:
	@./scripts/check-environment.sh

up:
	@./scripts/start-elasticsearch.sh single

down:
	@./scripts/stop-elasticsearch.sh

cluster-up:
	@./scripts/start-elasticsearch.sh cluster

cluster-down:
	@./scripts/stop-elasticsearch.sh

health:
	@echo "--> Checking cluster health:"
	@curl -s http://localhost:9200/_cluster/health?pretty || echo "Elasticsearch offline."
	@echo "\n--> Indices summary:"
	@curl -s "http://localhost:9200/_cat/indices?v" || true

reset-lab:
	@./scripts/reset-lab.sh

test:
	@echo "--> Running test suite across phases..."
	@python3 scripts/run-all-tests.py

clean:
	rm -rf __pycache__ tests/__pycache__ .pytest_cache outputs/temp_*
