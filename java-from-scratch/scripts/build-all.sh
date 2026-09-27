#!/usr/bin/env bash
# ==============================================================================
# java-from-scratch: Build All Modules
# Compiles all phases, exercises, projects, broken programs, and capstones
# ==============================================================================

set -euo pipefail

BOLD="\033[1m"
GREEN="\033[0;32m"
BLUE="\033[0;34m"
RESET="\033[0m"

echo -e "${BOLD}${BLUE}======================================================${RESET}"
echo -e "${BOLD}${BLUE}  java-from-scratch: Building Complete Repository    ${RESET}"
echo -e "${BOLD}${BLUE}======================================================${RESET}\n"

mvn clean compile -DskipTests

echo ""
echo -e "${BOLD}${GREEN}Build complete across all modules!${RESET}"
