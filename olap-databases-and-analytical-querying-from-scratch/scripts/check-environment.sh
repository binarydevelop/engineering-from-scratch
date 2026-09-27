#!/usr/bin/env bash
set -euo pipefail

BOLD="\033[1m"
GREEN="\033[0;32m"
YELLOW="\033[0;33m"
RED="\033[0;31m"
CYAN="\033[0;36m"
RESET="\033[0m"

echo -e "${BOLD}${CYAN}========================================================================${RESET}"
echo -e "${BOLD}${CYAN}   OLAP Databases & Analytical Querying Lab - Environment Check         ${RESET}"
echo -e "${BOLD}${CYAN}========================================================================${RESET}"

status_ok() {
    echo -e "  [${GREEN}✓ OK${RESET}] $1"
}

status_warn() {
    echo -e "  [${YELLOW}! WARN${RESET}] $1"
}

status_fail() {
    echo -e "  [${RED}✗ FAIL${RESET}] $1"
}

ERRORS=0

# 1. Check Python
echo -e "\n${BOLD}1. Checking Python Environment:${RESET}"
if command -v python3 >/dev/null 2>&1; then
    PY_VER=$(python3 --version 2>&1)
    status_ok "Python binary found: ${PY_VER}"
else
    status_fail "Python 3 not found on system PATH."
    ERRORS=$((ERRORS + 1))
fi

# 2. Check Virtual Environment & Packages
echo -e "\n${BOLD}2. Checking Python Modules & DB Connectors:${RESET}"
PYTHON_BIN=".venv/bin/python"
if [ ! -f "${PYTHON_BIN}" ]; then
    PYTHON_BIN="python3"
fi

if "${PYTHON_BIN}" -c "import duckdb, pyarrow, rich, tabulate" >/dev/null 2>&1; then
    DUCKDB_VER=$("${PYTHON_BIN}" -c "import duckdb; print(duckdb.__version__)")
    PYARROW_VER=$("${PYTHON_BIN}" -c "import pyarrow; print(pyarrow.__version__)")
    status_ok "DuckDB Python module: v${DUCKDB_VER}"
    status_ok "PyArrow Python module: v${PYARROW_VER}"
else
    status_fail "Required Python packages (duckdb, pyarrow, rich, tabulate) missing. Run 'make setup'."
    ERRORS=$((ERRORS + 1))
fi

if "${PYTHON_BIN}" -c "import clickhouse_connect, psycopg2" >/dev/null 2>&1; then
    status_ok "Database drivers (clickhouse-connect, psycopg2) ready."
else
    status_warn "clickhouse-connect or psycopg2 not installed in current interpreter."
fi

# 3. Check Docker & Container Runtime
echo -e "\n${BOLD}3. Checking Docker & Container Runtime:${RESET}"
if command -v docker >/dev/null 2>&1; then
    DOCKER_VER=$(docker --version)
    status_ok "Docker daemon CLI: ${DOCKER_VER}"
    if docker info >/dev/null 2>&1; then
        status_ok "Docker daemon is running and responsive."
    else
        status_fail "Docker daemon is not running. Please start Docker Desktop/daemon."
        ERRORS=$((ERRORS + 1))
    fi
else
    status_warn "Docker CLI not found. Containerized ClickHouse/PostgreSQL will be disabled (DuckDB remains fully functional)."
fi

# 4. Check Port Availability
echo -e "\n${BOLD}4. Checking Port Availability:${RESET}"
check_port() {
    local port=$1
    local name=$2
    if lsof -i :"$port" >/dev/null 2>&1; then
        status_warn "Port $port ($name) is currently bound by a process."
    else
        status_ok "Port $port ($name) is free."
    fi
}
check_port 8123 "ClickHouse HTTP"
check_port 9000 "ClickHouse Native"
check_port 5433 "PostgreSQL Comparison Lab"

# 5. Check Disk Space
echo -e "\n${BOLD}5. Checking Storage Capacity:${RESET}"
AVAIL_MB=$(df -k . | tail -1 | awk '{print int($4/1024)}')
if [ "$AVAIL_MB" -gt 5000 ]; then
    status_ok "Available disk space: ${AVAIL_MB} MB (sufficient for multi-million row datasets)"
else
    status_warn "Available disk space is low (${AVAIL_MB} MB). Keep datasets scaled to 'small' or 'medium'."
fi

echo -e "\n${BOLD}${CYAN}========================================================================${RESET}"
if [ $ERRORS -eq 0 ]; then
    echo -e "${BOLD}${GREEN}Environment verification PASSED! Lab is ready.${RESET}"
    exit 0
else
    echo -e "${BOLD}${RED}Environment verification found $ERRORS critical issues. Address them before proceeding.${RESET}"
    exit 1
fi
