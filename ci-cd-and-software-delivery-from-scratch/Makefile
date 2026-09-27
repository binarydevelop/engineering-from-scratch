# ==============================================================================
# CI/CD and Software Delivery from Scratch — Makefile
# Motto: Understand it. Build it. Test it. Package it. Verify it. Release it.
#        Deploy it. Observe it. Recover it. Automate it.
# ==============================================================================

SHELL := /bin/bash
.DEFAULT_GOAL := help

.PHONY: help
help: ## Show this help message
	@echo "========================================================================"
	@echo " CI/CD and Software Delivery from Scratch — Developer Targets"
	@echo "========================================================================"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

.PHONY: check-env
check-env: ## Verify local environment, tools, runtimes, and dependencies
	@./scripts/check-environment.sh

.PHONY: test
test: ## Run unit, integration, and contract tests for the sample service
	@./scripts/test.sh

.PHONY: build
build: ## Execute deterministic build producing versioned artifact
	@./scripts/build.sh

.PHONY: package
package: ## Package built artifact into an immutable distribution bundle
	@./scripts/package.sh

.PHONY: local-ci
local-ci: ## Run complete local CI pipeline simulation from scratch
	@./scripts/local-ci.sh

.PHONY: release
release: ## Generate release metadata, SBOM, provenance attestation, and changelog
	@./scripts/release.sh

.PHONY: rollback
rollback: ## Execute automated deployment rollback simulation
	@./scripts/rollback.sh

.PHONY: simulations
simulations: ## Run all interactive deployment, GitOps, and security simulators
	@python3 deployment-labs/deploy_simulator.py --strategy canary --steps 1,10,50,100
	@python3 gitops/gitops_reconciler.py --mode dry-run
	@python3 security-labs/oidc_simulator.py

.PHONY: run-benchmarks
run-benchmarks: ## Run pipeline duration, DAG, and caching benchmarks
	@python3 benchmarks/benchmark_pipeline.py

.PHONY: verify-broken-labs
verify-broken-labs: ## Verify all broken pipeline scenarios and validate solutions
	@python3 broken-pipelines/verify_all_labs.py

.PHONY: clean
clean: ## Clean generated build artifacts, temporary outputs, and test caches
	@rm -rf outputs/tmp outputs/test-results outputs/*.tar.gz outputs/*.json
	@rm -rf .pytest_cache reports/ *.sqlite3
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@echo "Clean completed."
