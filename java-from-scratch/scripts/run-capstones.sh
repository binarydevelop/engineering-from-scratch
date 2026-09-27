#!/usr/bin/env bash
# ==============================================================================
# java-from-scratch: Run Advanced JVM & Concurrency Capstones
# ==============================================================================

set -euo pipefail

BOLD="\033[1m"
GREEN="\033[0;32m"
BLUE="\033[0;34m"
YELLOW="\033[0;33m"
RESET="\033[0m"

echo -e "${BOLD}${BLUE}======================================================${RESET}"
echo -e "${BOLD}${BLUE}  java-from-scratch: Advanced Capstones Execution     ${RESET}"
echo -e "${BOLD}${BLUE}======================================================${RESET}\n"

echo -e "${YELLOW}Executing automated tests and benchmarks for all 5 capstones...${RESET}"
mvn test -pl capstones

echo ""
echo -e "${BOLD}${GREEN}All Capstones verified successfully!${RESET}"
