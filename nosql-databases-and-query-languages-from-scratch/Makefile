.PHONY: help env-check lab-start lab-stop seed-data reset-data grade test-simulations verify

PROFILE ?= all

help:
	@echo "NoSQL Databases & Query Languages From Scratch - Makefile"
	@echo ""
	@echo "Available Targets:"
	@echo "  make env-check         Verify host tools and listening database ports"
	@echo "  make lab-start         Start local database containers (PROFILE=mongo|cassandra|all)"
	@echo "  make lab-stop          Stop all laboratory containers"
	@echo "  make seed-data         Generate rich cross-paradigm JSON datasets in datasets/"
	@echo "  make reset-data        Reset and regenerate all local datasets"
	@echo "  make test-simulations  Run all 6 distributed systems and storage engine simulators"
	@echo "  make grade             Run query grader self-test"
	@echo "  make verify            Run complete repository verification suite"

env-check:
	@./scripts/check-environment.sh

lab-start:
	@./scripts/start-lab.sh $(PROFILE)

lab-stop:
	@./scripts/stop-lab.sh

seed-data:
	@python3 scripts/seed-data.py

reset-data:
	@./scripts/reset-data.sh

test-simulations:
	@python3 simulations/hash_partitioning_sim.py
	@python3 simulations/consistent_hashing_sim.py
	@python3 simulations/quorum_sim.py
	@python3 simulations/tiny_kv.py
	@python3 simulations/tiny_lsm.py
	@python3 simulations/conflict_resolution_sim.py
	@python3 simulations/hot_partition_sim.py

grade:
	@python3 scripts/grade-query.py

verify:
	@./scripts/verify-repository.sh
