.PHONY: help setup env-check docker-up docker-down docker-status data-small data-medium data-large test benchmark clean

PYTHON ?= .venv/bin/python
PIP ?= .venv/bin/pip
PYTEST ?= .venv/bin/pytest

help:
	@echo "OLAP Databases and Analytical Querying from Scratch"
	@echo ""
	@echo "Available commands:"
	@echo "  make setup          Create virtual environment and install pinned dependencies"
	@echo "  make env-check      Verify all database engines, drivers, and CLI tools"
	@echo "  make docker-up      Start containerized engines (ClickHouse 24.8, PostgreSQL 16.4)"
	@echo "  make docker-down    Stop all containers"
	@echo "  make docker-status  Check container status and database health checks"
	@echo "  make data-small     Generate 100K-row multi-domain test datasets"
	@echo "  make data-medium    Generate 1M-row production-scale analytical datasets"
	@echo "  make data-large     Generate 10M-row high-cardinality stress datasets"
	@echo "  make test           Execute analytical SQL test suite and validation scripts"
	@echo "  make benchmark      Run reproducible benchmarks comparing row vs columnar engines"
	@echo "  make clean          Remove temporary tables, scratch files, and python caches"

setup:
	python3 -m venv .venv
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	@echo "Setup complete. Environment ready."

env-check:
	chmod +x ./scripts/*.sh
	./scripts/check-environment.sh

docker-up:
	docker compose up -d
	@echo "Waiting for services to become healthy..."
	@sleep 5
	docker compose ps

docker-down:
	docker compose down

docker-status:
	docker compose ps

data-small:
	$(PYTHON) scripts/generate-data.py --scale small

data-medium:
	$(PYTHON) scripts/generate-data.py --scale medium

data-large:
	$(PYTHON) scripts/generate-data.py --scale large

test:
	$(PYTEST) tests/ -v

benchmark:
	$(PYTHON) scripts/benchmark.py --suite core

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf outputs/*.duckdb outputs/*.duckdb.wal outputs/*.parquet
