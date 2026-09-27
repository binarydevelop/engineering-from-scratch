# AI Systems From Scratch - Master Makefile
.PHONY: help setup test benchmark check-env check-gpu clean run-all

PYTHON := .venv/bin/python
PYTEST := .venv/bin/pytest

help:
	@echo "AI Systems From Scratch - Commands"
	@echo "  make setup        : Install dependencies in local virtualenv"
	@echo "  make check-env    : Validate local environment and hardware tier"
	@echo "  make check-gpu    : Inspect accelerator, CUDA/MPS memory and status"
	@echo "  make test         : Run automated test suite across all modules"
	@echo "  make benchmark    : Run standard inference & training benchmarks"
	@echo "  make broken-labs  : Run broken-system lab diagnostic test harness"
	@echo "  make clean        : Remove build caches, checkpoints, and temporary logs"

setup:
	@uv venv --python 3.12 .venv
	@uv pip install -e . --python $(PYTHON)

check-env:
	@bash scripts/check-environment.sh

check-gpu:
	@$(PYTHON) scripts/check-gpu.py

test:
	@$(PYTEST) compiler-labs/ kernels/ training/ inference/ datasets/ agents/ tools/ evaluation/

broken-labs:
	@$(PYTHON) broken-systems/run_all_diagnostics.py

benchmark:
	@$(PYTHON) scripts/benchmark.py

clean:
	@bash scripts/cleanup.sh
