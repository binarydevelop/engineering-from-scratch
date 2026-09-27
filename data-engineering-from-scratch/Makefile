.PHONY: help setup check-env generate-data test test-phases test-projects test-broken test-exercises up down clean reset

PYTHON := .venv/bin/python
PIP := .venv/bin/pip
PYTEST := .venv/bin/pytest

help:
	@echo "Data Engineering From Scratch"
	@echo "Motto: Understand it. Ingest it. Model it. Transform it. Validate it. Break it. Recover it. Scale it. Operate it."
	@echo ""
	@echo "Available commands:"
	@echo "  make setup          - Set up virtual environment and install dependencies"
	@echo "  make check-env      - Run the environment verification script"
	@echo "  make generate-data  - Generate synthetic source datasets (CSV, JSON, Parquet)"
	@echo "  make test           - Run full test suite across all modules"
	@echo "  make test-phases    - Run tests for all educational phases"
	@echo "  make test-projects  - Run tests for end-to-end projects"
	@echo "  make test-broken    - Run tests verifying broken-pipeline lab scenarios"
	@echo "  make test-exercises - Run tests verifying exercise solutions"
	@echo "  make up             - Start local PostgreSQL & MinIO Docker services"
	@echo "  make down           - Stop local Docker containers"
	@echo "  make clean          - Remove temporary artifacts and cache directories"
	@echo "  make reset          - Reset local lab datasets and database tables"

setup:
	python3 -m venv .venv
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

check-env:
	bash scripts/check-environment.sh

generate-data:
	$(PYTHON) scripts/generate-data.py

test:
	$(PYTEST) phases projects broken-pipelines exercises

test-phases:
	$(PYTEST) phases

test-projects:
	$(PYTEST) projects

test-broken:
	$(PYTEST) broken-pipelines

test-exercises:
	$(PYTEST) exercises

up:
	docker compose up -d

down:
	docker compose down -v

clean:
	rm -rf .pytest_cache __pycache__ */__pycache__ */*/__pycache__ outputs/runs data/runtime *.duckdb *.duckdb.wal

reset: clean
	bash scripts/reset-lab.sh
