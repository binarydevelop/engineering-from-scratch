# Makefile for docker-from-scratch
# NOTE: Make is merely a convenience task runner. 
# Do not treat Make as a replacement for learning the underlying Docker CLI commands!

.DEFAULT_GOAL := help
SHELL := /bin/bash

.PHONY: help
help: ## Show this help message
	@echo "docker-from-scratch automation commands:"
	@echo "----------------------------------------"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

.PHONY: verify
verify: ## Verify host environment and Docker engine connectivity
	@./scripts/verify_env.sh

.PHONY: test
test: ## Run validation checks across all curriculum lessons
	@./scripts/run_all_checks.sh

.PHONY: clean
clean: ## Safely tear down all lab containers, networks, and volumes
	@./scripts/clean_labs.sh

.PHONY: capstone-build
capstone-build: ## Build the Phase 29 Capstone multi-service application
	docker compose -f projects/capstone-system-lab/docker-compose.yml build

.PHONY: capstone-up
capstone-up: ## Launch the Phase 29 Capstone multi-service system
	docker compose -f projects/capstone-system-lab/docker-compose.yml up -d

.PHONY: capstone-down
capstone-down: ## Stop and remove the Phase 29 Capstone multi-service system
	docker compose -f projects/capstone-system-lab/docker-compose.yml down -v
