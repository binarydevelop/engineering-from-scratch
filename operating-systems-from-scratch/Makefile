# Operating Systems From Scratch: Master Makefile
CC ?= gcc
CFLAGS = -Wall -Wextra -pedantic -std=c11 -pthread -O2

.PHONY: all build test check-env clean capstones benchmarks labs help

all: build

help:
	@echo "Operating Systems From Scratch: Build Targets"
	@echo "  make check-env   - Verify host platform, tools, and kernel readiness"
	@echo "  make build       - Compile all benchmarks, capstones, and solutions"
	@echo "  make test        - Run complete automated test suite"
	@echo "  make capstones   - Build all 6 capstone projects"
	@echo "  make benchmarks  - Compile all performance benchmarks"
	@echo "  make clean       - Remove compiled binaries and temporary test artifacts"

check-env:
	@./scripts/check-environment.sh

build:
	@./scripts/build-all.sh

test: build
	@./scripts/run-tests.sh

capstones:
	@$(MAKE) -C projects/01-tiny-shell
	@$(MAKE) -C projects/05-event-http-server
	@$(MAKE) -C projects/06-container-sandbox

benchmarks:
	@mkdir -p bin
	@for b in benchmarks/*.c; do \
		name=$$(basename $$b .c); \
		echo "Compiling benchmark: $$name"; \
		$(CC) $(CFLAGS) $$b -o bin/$$name; \
	done

clean:
	@./scripts/cleanup.sh
	@$(MAKE) -C projects/01-tiny-shell clean
	@$(MAKE) -C projects/05-event-http-server clean
	@$(MAKE) -C projects/06-container-sandbox clean
