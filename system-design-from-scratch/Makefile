.PHONY: help setup env-check test test-phases test-simulations test-broken test-projects test-problems test-calculations test-architectures test-experiments clean

PYTHON ?= .venv/bin/python
PYTEST ?= .venv/bin/pytest

help:
	@echo "System Design From Scratch - Automation Hub"
	@echo ""
	@echo "Available Targets:"
	@echo "  make setup             Create virtualenv and install dependencies"
	@echo "  make env-check         Verify Python, toolchain, and mathematical libraries"
	@echo "  make test              Run the complete master test suite (all modules)"
	@echo "  make test-phases       Run verification tests across all curriculum phases"
	@echo "  make test-simulations  Run unit and invariant tests across executable simulators"
	@echo "  make test-broken       Run reproduction and fix tests for broken architecture labs"
	@echo "  make test-projects     Run tests for substantial standalone project architectures"
	@echo "  make test-problems     Run tests for interview design problems and solutions"
	@echo "  make test-calculations Run tests for back-of-the-envelope estimation drills"
	@echo "  make test-architectures Run tests for architecture evolution case studies"
	@echo "  make test-experiments  Run tests for failure injection and chaos experiments"
	@echo "  make clean             Reset databases, caches, and test artifacts"

setup:
	@which uv >/dev/null 2>&1 && uv venv .venv --python 3.12 && uv pip install --python .venv/bin/python -r requirements.txt || python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
	@echo "Setup complete! Activate with: source .venv/bin/activate"

env-check:
	@bash scripts/check-environment.sh

test:
	$(PYTEST) phases/ simulations/ broken-systems/ projects/ interview-problems/ calculations/ architectures/ experiments/

test-phases:
	$(PYTEST) phases/

test-simulations:
	$(PYTEST) simulations/

test-broken:
	$(PYTEST) broken-systems/

test-projects:
	$(PYTEST) projects/

test-problems:
	$(PYTEST) interview-problems/

test-calculations:
	$(PYTEST) calculations/

test-architectures:
	$(PYTEST) architectures/

test-experiments:
	$(PYTEST) experiments/

clean:
	@bash scripts/reset-lab.sh
