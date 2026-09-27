#!/usr/bin/env bash
# ==============================================================================
# Environment Verification Script: Data Engineering From Scratch
# ==============================================================================
set -euo pipefail

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}======================================================${NC}"
echo -e "${BLUE}    Data Engineering From Scratch - Environment Check ${NC}"
echo -e "${BLUE}======================================================${NC}"

ALL_PASSED=true

# 1. Check Python Version
echo -n "Checking Python (>= 3.11)... "
if command -v python3 &> /dev/null; then
    PY_VER=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")')
    PY_MAJOR=$(python3 -c 'import sys; print(sys.version_info.major)')
    PY_MINOR=$(python3 -c 'import sys; print(sys.version_info.minor)')
    if [ "$PY_MAJOR" -ge 3 ] && [ "$PY_MINOR" -ge 11 ]; then
        echo -e "${GREEN}OK (${PY_VER})${NC}"
    else
        echo -e "${RED}FAIL (Found ${PY_VER}, requires >= 3.11)${NC}"
        ALL_PASSED=false
    fi
else
    echo -e "${RED}FAIL (python3 not found)${NC}"
    ALL_PASSED=false
fi

# 2. Check Virtual Environment or Python Packages
echo -n "Checking Python Dependencies (DuckDB, PyArrow, Pydantic, Pytest)... "
PYTHON_BIN="python3"
if [ -f ".venv/bin/python" ]; then
    PYTHON_BIN=".venv/bin/python"
fi

if $PYTHON_BIN -c "import duckdb, pyarrow, pydantic, pytest, rich, sqlparse, tabulate" 2> /dev/null; then
    DUCKDB_VER=$($PYTHON_BIN -c 'import duckdb; print(duckdb.__version__)')
    ARROW_VER=$($PYTHON_BIN -c 'import pyarrow; print(pyarrow.__version__)')
    echo -e "${GREEN}OK (DuckDB ${DUCKDB_VER}, PyArrow ${ARROW_VER})${NC}"
else
    echo -e "${YELLOW}WARNING (Missing some Python packages. Run: make setup)${NC}"
fi

# 3. Check Docker
echo -n "Checking Docker... "
if command -v docker &> /dev/null; then
    DOCKER_VER=$(docker --version | awk '{print $3}' | tr -d ',')
    echo -e "${GREEN}OK (${DOCKER_VER})${NC}"
else
    echo -e "${YELLOW}OPTIONAL: Docker not found. Local Python & DuckDB labs will work without Docker.${NC}"
fi

# 4. Check Disk Space
echo -n "Checking Available Disk Space (> 2 GB recommended)... "
FREE_KB=$(df -k . | awk 'NR==2 {print $4}')
FREE_GB=$((FREE_KB / 1024 / 1024))
if [ "$FREE_GB" -ge 2 ]; then
    echo -e "${GREEN}OK (${FREE_GB} GB available)${NC}"
else
    echo -e "${YELLOW}LOW DISK SPACE (${FREE_GB} GB available). Clean up to avoid file I/O errors.${NC}"
fi

# 5. Check Working Directory Structure
echo -n "Checking Repository Directories... "
for dir in datasets pipelines transformations schemas broken-pipelines projects docs; do
    if [ ! -d "$dir" ]; then
        mkdir -p "$dir"
    fi
done
echo -e "${GREEN}OK${NC}"

echo -e "${BLUE}======================================================${NC}"
if [ "$ALL_PASSED" = true ]; then
    echo -e "${GREEN}Environment is ready! You can now run 'make generate-data' and start Lesson 00.${NC}"
else
    echo -e "${RED}Environment check failed. Please resolve the errors above.${NC}"
    exit 1
fi
