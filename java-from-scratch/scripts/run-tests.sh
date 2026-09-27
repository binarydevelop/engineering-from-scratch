#!/usr/bin/env bash
# ==============================================================================
# java-from-scratch: Run Test Suite
# Runs automated JUnit 5 tests across all modules
# ==============================================================================

set -euo pipefail

BOLD="\033[1m"
GREEN="\033[0;32m"
BLUE="\033[0;34m"
RESET="\033[0m"

echo -e "${BOLD}${BLUE}======================================================${RESET}"
echo -e "${BOLD}${BLUE}  java-from-scratch: Running Automated Test Suites   ${RESET}"
echo -e "${BOLD}${BLUE}======================================================${RESET}\n"

mvn test

echo ""
echo -e "${BOLD}${GREEN}All test suites passed successfully!${RESET}"
