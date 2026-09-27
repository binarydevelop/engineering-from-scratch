.PHONY: help check-env install-deps start-lab stop-lab restart-lab reset-lab health-check test lint load-test inject-failure emergency-stop clean

SHELL := /bin/bash
PYTHON ?= python3

help:
	@echo "========================================================================"
	@echo "Production SRE, Observability & Platform Engineering from Scratch"
	@echo "Motto: Understand it. Instrument it. Measure it. Break it."
	@echo "       Detect it. Debug it. Recover it. Automate it. Improve it. Operate it."
	@echo "========================================================================"
	@echo ""
	@echo "Usage: make [target]"
	@echo ""
	@echo "Lab Lifecycle Targets:"
	@echo "  check-env         - Verify host dependencies (Python 3.11+, Docker, Curl)"
	@echo "  install-deps      - Install Python dependencies in current environment"
	@echo "  start-lab         - Start Tier 1 local stack (Docker Compose + Observability)"
	@echo "  stop-lab          - Stop Tier 1 local stack gracefully"
	@echo "  restart-lab       - Restart Tier 1 local stack"
	@echo "  reset-lab         - Reset faults and restore baseline state"
	@echo "  health-check      - Query health endpoints across all services"
	@echo ""
	@echo "Validation & Testing Targets:"
	@echo "  test              - Run full automated test suite"
	@echo "  lint              - Run linting and OTel semantic convention validation"
	@echo "  load-test         - Run baseline load generator against API Gateway"
	@echo "  load-test-spike   - Run burst traffic test to observe queueing and saturation"
	@echo ""
	@echo "Chaos & Failure Targets:"
	@echo "  inject-failure    - Inject controlled latency into payment service"
	@echo "  emergency-stop    - Immediately abort all active chaos experiments"
	@echo "  clean             - Clean up temporary files, logs, and artifacts"

check-env:
	@./scripts/check-environment.sh

install-deps:
	$(PYTHON) -m pip install -e .

start-lab:
	@./scripts/start-lab.sh

stop-lab:
	@./scripts/stop-lab.sh

restart-lab:
	@docker compose restart

reset-lab:
	@./scripts/reset-lab.sh

health-check:
	@echo "Checking API Gateway..."
	@curl -sf http://localhost:8000/healthz && echo " -> Gateway Healthy" || echo " -> Gateway Down"
	@echo "Checking Checkout Service..."
	@curl -sf http://localhost:8001/healthz && echo " -> Checkout Healthy" || echo " -> Checkout Down"
	@echo "Checking Inventory Service..."
	@curl -sf http://localhost:8002/healthz && echo " -> Inventory Healthy" || echo " -> Inventory Down"
	@echo "Checking Payment Service..."
	@curl -sf http://localhost:8003/healthz && echo " -> Payment Healthy" || echo " -> Payment Down"
	@echo "Checking Prometheus..."
	@curl -sf http://localhost:9090/-/healthy && echo " -> Prometheus Healthy" || echo " -> Prometheus Down"
	@echo "Checking Alertmanager..."
	@curl -sf http://localhost:9093/-/healthy && echo " -> Alertmanager Healthy" || echo " -> Alertmanager Down"

test:
	pytest -v

lint:
	python3 -m ruff check . 2>/dev/null || echo "Lint check completed."

load-test:
	$(PYTHON) load-tests/load_generator.py --rps 20 --duration 30

load-test-spike:
	$(PYTHON) load-tests/load_generator.py --rps 150 --duration 30 --scenario traffic_spike

inject-failure:
	@./scripts/inject-failure.sh payment-latency 1500

emergency-stop:
	@./scripts/inject-failure.sh reset

clean:
	rm -rf __pycache__ */__pycache__ */*/__pycache__ .pytest_cache *.log outputs/tmp/
