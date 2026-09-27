#!/usr/bin/env bash
# ==============================================================================
# java-from-scratch: Run Broken Program Diagnostics Harness
# ==============================================================================

set -euo pipefail

BOLD="\033[1m"
GREEN="\033[0;32m"
BLUE="\033[0;34m"
YELLOW="\033[0;33m"
RESET="\033[0m"

echo -e "${BOLD}${BLUE}======================================================${RESET}"
echo -e "${BOLD}${BLUE}  java-from-scratch: Broken Program Diagnostics Harness${RESET}"
echo -e "${BOLD}${BLUE}======================================================${RESET}\n"

echo -e "${YELLOW}Executing diagnostic verification for broken programs and fixes...${RESET}"
mvn test -pl broken-programs

echo ""
echo -e "${BOLD}${GREEN}Broken programs diagnostic verification completed successfully!${RESET}"
