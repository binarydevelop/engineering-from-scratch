.PHONY: all help check test lab-up lab-down clean build-c docker-lab

PYTHON ?= python3

all: help

help:
	@echo "computer-networking-from-scratch automation commands:"
	@echo "  make check       - Verify host environment and required network tools"
	@echo "  make test        - Run all simulation, socket, and project test suites"
	@echo "  make build-c     - Compile C socket programs (socket-programs/c)"
	@echo "  make lab-up      - Create isolated Linux network namespace testbed (requires sudo on Linux)"
	@echo "  make lab-down    - Destroy isolated Linux network namespace testbed"
	@echo "  make docker-lab  - Run tests inside an isolated Linux container (cross-platform)"
	@echo "  make clean       - Remove compiled binaries, pcaps, and temporary python files"

check:
	@chmod +x scripts/*.sh
	@./scripts/check-environment.sh

test:
	@echo "==> Running Python simulation & project tests..."
	@$(PYTHON) ./scripts/run-all-tests.py

build-c:
	@echo "==> Compiling C socket programs..."
	@$(MAKE) -C socket-programs/c all

lab-up:
	@echo "==> Creating isolated Linux network namespace lab..."
	@sudo ./scripts/create-network-lab.sh

lab-down:
	@echo "==> Dismantling network namespace lab..."
	@sudo ./scripts/destroy-network-lab.sh

docker-lab:
	@echo "==> Running complete test and namespace suite in isolated Docker container..."
	@./scripts/run-docker-lab.sh

clean:
	@echo "==> Cleaning build artifacts and cache..."
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@find . -type f -name "*.pyc" -delete
	@find . -type f -name "*.pcap" -delete
	@find . -type f -name "*.log" -delete
	@$(MAKE) -C socket-programs/c clean 2>/dev/null || true
	@echo "Clean completed."
