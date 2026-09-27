.PHONY: help env up down restart psql reset seed seed-ecommerce seed-social seed-saas seed-banking seed-analytics grade drills test benchmark clean

# Default target
help:
	@echo "======================================================================"
	@echo " DATABASE AND SQL FROM SCRATCH: Developer Automation & Lab Harness"
	@echo " Understand it. Model it. Query it. Inspect it. Measure it."
	@echo " Break it. Fix it. Optimize it. Ship it."
	@echo "======================================================================"
	@echo "Environment & Services:"
	@echo "  make env              - Check local tools (docker, psql, python)"
	@echo "  make up               - Start pinned PostgreSQL 16 container"
	@echo "  make down             - Stop PostgreSQL container"
	@echo "  make restart          - Restart PostgreSQL container"
	@echo "  make psql             - Open interactive psql terminal to sqllab"
	@echo ""
	@echo "Database Lifecycle & Datasets:"
	@echo "  make reset            - Drop and recreate all lab schemas"
	@echo "  make seed             - Seed all 5 datasets (ecommerce, social, saas, banking, analytics)"
	@echo "  make seed-ecommerce   - Seed e-commerce dataset only"
	@echo "  make seed-social      - Seed social network dataset only"
	@echo "  make seed-saas        - Seed SaaS multi-tenant dataset only"
	@echo "  make seed-banking     - Seed transactional banking dataset only"
	@echo "  make seed-analytics   - Seed web/event analytics dataset only"
	@echo ""
	@echo "Verification & Mastery:"
	@echo "  make grade QUERY=<f>  - Grade a single learner query against reference"
	@echo "  make drills           - Test and grade all 50 drills"
	@echo "  make test             - Run python project tests (mini-db, tiny-planner, app)"
	@echo "  make benchmark        - Run sequential scan vs B-tree benchmark suite"
	@echo "======================================================================"

env:
	@bash scripts/check-environment.sh

up:
	@bash scripts/start-db.sh

down:
	@bash scripts/stop-db.sh

restart: down up

psql:
	@docker exec -it database-sql-scratch-db psql -U postgres -d sqllab

reset:
	@bash scripts/reset-db.sh

seed:
	@bash scripts/seed-db.sh all

seed-ecommerce:
	@bash scripts/seed-db.sh ecommerce

seed-social:
	@bash scripts/seed-db.sh social

seed-saas:
	@bash scripts/seed-db.sh saas

seed-banking:
	@bash scripts/seed-db.sh banking

seed-analytics:
	@bash scripts/seed-db.sh analytics

grade:
	@python3 scripts/grade-query.py $(QUERY)

drills:
	@python3 scripts/grade-query.py --all-drills

test:
	@pytest projects/

benchmark:
	@python3 benchmarks/run_benchmarks.py

clean:
	@rm -rf __pycache__ .pytest_cache outputs/tmp/*.log
