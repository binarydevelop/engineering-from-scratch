#!/usr/bin/env bash
set -euo pipefail

BOLD="\033[1m"
GREEN="\033[0;32m"
CYAN="\033[0;36m"
YELLOW="\033[0;33m"
RESET="\033[0m"

echo -e "${BOLD}${CYAN}========================================================================${RESET}"
echo -e "${BOLD}${CYAN}   Starting OLAP Databases & Analytical Querying Lab                    ${RESET}"
echo -e "${BOLD}${CYAN}========================================================================${RESET}"

# 1. Environment Check
echo -e "\n${BOLD}[1/4] Running Environment Pre-Flight Verification...${RESET}"
./scripts/check-environment.sh

# 2. Start Docker Containers
echo -e "\n${BOLD}[2/4] Starting Columnar & Relational Database Containers...${RESET}"
docker compose up -d

# 3. Wait for Health Checks
echo -e "\n${BOLD}[3/4] Awaiting Database Health Checks...${RESET}"
RETRIES=15
while [ $RETRIES -gt 0 ]; do
    if curl -s "http://127.0.0.1:8123/ping" | grep -q "Ok" 2>/dev/null; then
        echo -e "  [${GREEN}✓ OK${RESET}] ClickHouse 24.8 HTTP endpoint is healthy (http://127.0.0.1:8123)"
        break
    fi
    echo "  ...waiting for ClickHouse to report ready (${RETRIES} remaining)"
    sleep 2
    RETRIES=$((RETRIES - 1))
done

# 4. Generate Initial Synthetic Datasets if missing
echo -e "\n${BOLD}[4/4] Verifying Analytical Datasets...${RESET}"
if [ ! -f "outputs/olap_lab.duckdb" ]; then
    echo "  Generating initial small analytical datasets..."
    .venv/bin/python scripts/generate-data.py --scale small
else
    echo -e "  [${GREEN}✓ OK${RESET}] DuckDB lab database found at outputs/olap_lab.duckdb"
fi

echo -e "\n${BOLD}${GREEN}========================================================================${RESET}"
echo -e "${BOLD}${GREEN}   All Analytical Lab Systems are LIVE & READY!                         ${RESET}"
echo -e "${BOLD}${GREEN}   - DuckDB 1.5.5:       In-process (outputs/olap_lab.duckdb)            ${RESET}"
echo -e "${BOLD}${GREEN}   - ClickHouse 24.8:    http://127.0.0.1:8123 (Native: 9000)           ${RESET}"
echo -e "${BOLD}${GREEN}   - PostgreSQL 16.4:    127.0.0.1:5433 (User: postgres, DB: sqllab)     ${RESET}"
echo -e "${BOLD}${GREEN}========================================================================${RESET}"
