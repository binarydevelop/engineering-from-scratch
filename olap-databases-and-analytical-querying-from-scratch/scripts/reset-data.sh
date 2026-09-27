#!/usr/bin/env bash
set -euo pipefail

BOLD="\033[1m"
RED="\033[0;31m"
GREEN="\033[0;32m"
RESET="\033[0m"

SCALE="${1:-small}"

echo -e "${BOLD}${RED}[!] Resetting and purging generated datasets and databases...${RESET}"
rm -rf outputs/*.duckdb outputs/*.duckdb.wal
rm -rf datasets/*/*.parquet datasets/*/*.csv

echo -e "${BOLD}[*] Regenerating fresh datasets (scale: ${SCALE})...${RESET}"
.venv/bin/python scripts/generate-data.py --scale "${SCALE}"

echo -e "${BOLD}${GREEN}[✓] Data reset complete. Clean state restored.${RESET}"
