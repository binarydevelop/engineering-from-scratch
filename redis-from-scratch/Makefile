# ==============================================================================
# redis-from-scratch Makefile
#
# IMPORTANT PEDAGOGICAL PRINCIPLE:
# Make != Redis != Docker
#
# These targets are convenience shortcuts for everyday laboratory workflows.
# Never rely on them blindly without understanding the underlying commands
# printed in each recipe.
# ==============================================================================

.PHONY: help env-check start-local stop-local up down reset-lab test clean

help:
	@echo "redis-from-scratch - Laboratory Automation"
	@echo "=========================================="
	@echo "Convenience targets (see Makefile for underlying commands):"
	@echo "  make env-check    : Verify Python, Docker, Redis-CLI, and networking tools"
	@echo "  make up           : Launch Redis primary & Postgres via docker compose"
	@echo "  make down         : Stop and remove docker containers"
	@echo "  make start-local  : Start host redis-server in the background on port 6379"
	@echo "  make stop-local   : Terminate host redis-server"
	@echo "  make reset-lab    : FLUSHALL keys, clean runtime RDB/AOF dumps, reset state"
	@echo "  make test         : Run automated validation test suite across all phases"

env-check:
	@echo "--> Executing: ./scripts/check-environment.sh"
	@./scripts/check-environment.sh

up:
	@echo "--> Executing: docker compose up -d redis-primary postgres"
	docker compose up -d redis-primary postgres
	@echo "Redis primary is running on port 6379 (Docker)"

down:
	@echo "--> Executing: docker compose down"
	docker compose down

start-local:
	@echo "--> Executing: ./scripts/start-redis.sh local"
	@./scripts/start-redis.sh local

stop-local:
	@echo "--> Executing: ./scripts/stop-redis.sh local"
	@./scripts/stop-redis.sh local

reset-lab:
	@echo "--> Executing: ./scripts/reset-lab.sh"
	@./scripts/reset-lab.sh

test:
	@echo "--> Running validation suite across all phases..."
	python3 -m unittest discover -s tests -p "*_test.py" 2>/dev/null || python3 scripts/run-all-tests.py

clean:
	@echo "--> Cleaning temporary files, caches, and test dumps..."
	rm -rf *.rdb *.aof appendonlydir/ __pycache__ .pytest_cache
