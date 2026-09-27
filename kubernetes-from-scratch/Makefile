.PHONY: help check cluster-up cluster-down status reset lint test-controller test-scheduler test-bin-packing test-mini-k8s test-all

CLUSTER_NAME ?= k8s-scratch-cluster

help:
	@echo "kubernetes-from-scratch: Available Targets"
	@echo "--------------------------------------------------------"
	@echo "  make check              - Verify CLI tools, docker daemon, and versions"
	@echo "  make cluster-up         - Provision 3-node kind cluster (v1.37.0)"
	@echo "  make cluster-down       - Delete kind cluster and clean context"
	@echo "  make status             - Inspect control plane and node topology"
	@echo "  make reset              - Clean test workloads and restore baseline"
	@echo "  make lint               - Validate YAML manifests with kubectl dry-run"
	@echo "  make test-controller    - Run Phase 02 mini reconciler test suite"
	@echo "  make test-scheduler     - Run Phase 10 scheduler simulator"
	@echo "  make test-bin-packing   - Run Phase 105 bin packing simulator"
	@echo "  make test-mini-k8s      - Run Phase 117 Mini Kubernetes test suite"
	@echo "  make test-all           - Run all automated code suites"
	@echo "--------------------------------------------------------"

check:
	./scripts/check-environment.sh

cluster-up:
	./scripts/create-cluster.sh $(CLUSTER_NAME)

cluster-down:
	./scripts/destroy-cluster.sh $(CLUSTER_NAME)

status:
	./scripts/cluster-status.sh

reset:
	./scripts/reset-lab.sh

lint:
	@echo "Validating all manifests against Kubernetes API..."
	@find manifests projects phases -name "*.yaml" -o -name "*.yml" | while read -r f; do \
		echo "Validating $$f"; \
		kubectl apply --dry-run=client -f "$$f" >/dev/null || exit 1; \
	done
	@echo "All manifests validated successfully!"

test-controller:
	python3 phases/02-desired-state/code/mini_controller.py --test

test-scheduler:
	python3 phases/10-scheduling-from-scratch/code/scheduler_sim.py

test-bin-packing:
	python3 phases/105-bin-packing/code/bin_packing_sim.py

test-mini-k8s:
	python3 projects/09-build-mini-kubernetes/code/mini_k8s.py --test

test-all: test-controller test-scheduler test-bin-packing test-mini-k8s
	@echo "All educational code tests passed!"
