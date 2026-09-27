.PHONY: help check test-scripts reset clean

help:
	@echo "linux-from-scratch Automation Makefile"
	@echo "---------------------------------------"
	@echo "make check         - Validate local Linux environment"
	@echo "make test-scripts  - Lint all shell scripts using shellcheck"
	@echo "make reset         - Reset all lab sandboxes and loop mounts"
	@echo "make clean         - Safely remove temporary lab artifacts"

check:
	@bash scripts/check-environment.sh

test-scripts:
	@which shellcheck >/dev/null 2>&1 && shellcheck scripts/*.sh broken-systems/*/*.sh || echo "Notice: shellcheck not installed. Skipping linting."

reset:
	@bash scripts/reset-lab.sh

clean:
	@bash scripts/cleanup.sh
