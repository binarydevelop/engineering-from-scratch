# ==============================================================================
# aws-from-scratch: Developer & Learner Automation
# ==============================================================================
# IMPORTANT ARCHITECTURAL REALIZATION:
# Make != Terraform != AWS CLI != AWS APIs
#
# When you type:          make test-iam
# Make runs:              python3 experiments/iam_simulator.py
#
# When you type:          make check-identity
# Make runs:              aws sts get-caller-identity
# Which sends:            HTTPS POST / HTTP 1.1 with SigV4 signature to:
#                         https://sts.amazonaws.com
#
# Never let a Makefile obscure the network calls and APIs underneath!
# ==============================================================================

.PHONY: help check-env check-identity list-resources cleanup-check test test-simulators lint clean

help:
	@echo "aws-from-scratch: Educational Cloud Engineering Lab"
	@echo "=================================================="
	@echo "Available commands:"
	@echo "  make check-env        - Verify Python, AWS CLI, Docker, and utilities"
	@echo "  make check-identity   - Interrogate AWS STS and verify caller identity & security"
	@echo "  make list-resources   - Scan AWS account for active lab resources (read-only)"
	@echo "  make cleanup-check    - Verify account is clean and zero-cost"
	@echo "  make test-simulators  - Run local simulations (IAM, Queues, Load Balancer, Cloud Sim)"
	@echo "  make test             - Run complete automated test suite"
	@echo "  make clean            - Remove local Python caches, test logs, and temp artifacts"

check-env:
	@bash scripts/check-environment.sh

check-identity:
	@bash scripts/check-aws-identity.sh

list-resources:
	@bash scripts/list-lab-resources.sh

cleanup-check:
	@bash scripts/cleanup-check.sh

test-simulators:
	@echo "==> Running IAM Evaluator Simulation (Phase 03)..."
	@python3 experiments/iam_simulator.py
	@echo "==> Running Load Balancer Simulation (Phase 22)..."
	@python3 experiments/lb_healthcheck_lab.py
	@echo "==> Running SQS Visibility Lab (Phase 34)..."
	@python3 experiments/sqs_visibility_lab.py
	@echo "==> Running Tiny Cloud Simulator (Phase 81)..."
	@python3 projects/project-07-tiny-cloud-simulator/tiny_cloud.py

test:
	@python3 -m unittest discover -s tests -p "test_*.py" -v

clean:
	@rm -rf __pycache__ */__pycache__ */*/__pycache__ .pytest_cache .coverage htmlcov
	@rm -rf outputs/*.log scratch/
	@echo "✓ Cleaned local caches and temporary artifacts."
