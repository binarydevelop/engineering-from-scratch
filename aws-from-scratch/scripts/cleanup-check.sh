#!/usr/bin/env bash
# ==============================================================================
# scripts/cleanup-check.sh
# Verifies that all lab resources have been torn down and the account is clean.
# ==============================================================================

set -euo pipefail

BOLD="\033[1m"
GREEN="\033[0;32m"
YELLOW="\033[0;33m"
RED="\033[0;31m"
BLUE="\033[0;34m"
RESET="\033[0m"

echo -e "${BLUE}${BOLD}=====================================================${RESET}"
echo -e "${BLUE}${BOLD}      aws-from-scratch: Post-Lab Cleanup Check       ${RESET}"
echo -e "${BLUE}${BOLD}=====================================================${RESET}"
echo ""

# Delegate to list-lab-resources.sh
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ -f "$SCRIPT_DIR/list-lab-resources.sh" ]; then
    bash "$SCRIPT_DIR/list-lab-resources.sh"
else
    echo -e "${RED}Error: $SCRIPT_DIR/list-lab-resources.sh not found.${RESET}"
    exit 1
fi
