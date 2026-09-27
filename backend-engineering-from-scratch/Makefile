.PHONY: help setup env-check test test-phases test-projects test-broken benchmarks load-test clean

PYTHON ?= .venv/bin/python
PYTEST ?= .venv/bin/pytest

help:
	@echo "Backend Engineering From Scratch - Command Center"
	@echo ""
	@echo "Targets:"
	@echo "  make setup          Create virtualenv and install dependencies"
	@echo "  make env-check      Verify development environment, Python, and tools"
	@echo "  make test           Run all pytest test suites (phases, projects, broken-systems)"
	@echo "  make test-phases    Run unit and integration tests across core phases"
	@echo "  make test-projects  Run test suites for all 13 standalone projects"
	@echo "  make test-broken    Run reproduction and verification tests for broken systems"
	@echo "  make test-apps      Run test suites for all 4 capstone applications"
	@echo "  make benchmarks     Execute latency, throughput, and connection benchmarks"
	@echo "  make load-test      Run async load test scenarios"
	@echo "  make clean          Clean temporary files, caches, and test artifacts"

setup:
	@which uv >/dev/null 2>&1 && uv venv .venv --python 3.12 && uv pip install --python .venv/bin/python -r requirements.txt || python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
	@echo "Setup complete! Activate with: source .venv/bin/activate"

env-check:
	@bash scripts/check-environment.sh

test:
	$(PYTEST) phases/ projects/ broken-systems/ apps/

test-phases:
	$(PYTEST) phases/

test-projects:
	$(PYTEST) projects/

test-broken:
	$(PYTEST) broken-systems/

test-apps:
	$(PYTEST) apps/

benchmarks:
	$(PYTHON) benchmarks/run_all_benchmarks.py

load-test:
	$(PYTHON) load-tests/scenarios/orders_spike.py
	$(PYTHON) load-tests/scenarios/read_heavy_traffic.py

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.db" -delete
	find . -type f -name "*.sqlite3" -delete
	rm -rf .pytest_cache .coverage htmlcov
