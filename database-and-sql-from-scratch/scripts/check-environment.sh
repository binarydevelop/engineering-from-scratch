#!/usr/bin/env bash
set -euo pipefail

echo "======================================================================"
echo " DATABASE AND SQL FROM SCRATCH: Environment Diagnostic"
echo "======================================================================"

EXIT_CODE=0

# 1. Check Docker
echo -n "Checking Docker daemon... "
if command -v docker >/dev/null 2>&1; then
    if docker info >/dev/null 2>&1; then
        DOCKER_VER=$(docker --version | awk '{print $3}' | tr -d ',')
        echo "OK (Docker $DOCKER_VER)"
    else
        echo "WARNING: Docker CLI installed, but daemon is not running."
        EXIT_CODE=1
    fi
else
    echo "MISSING: docker not found on PATH."
    EXIT_CODE=1
fi

# 2. Check Docker Compose
echo -n "Checking Docker Compose... "
if docker compose version >/dev/null 2>&1; then
    COMPOSE_VER=$(docker compose version --short)
    echo "OK (Docker Compose $COMPOSE_VER)"
elif command -v docker-compose >/dev/null 2>&1; then
    COMPOSE_VER=$(docker-compose --version | awk '{print $3}' | tr -d ',')
    echo "OK (docker-compose $COMPOSE_VER)"
else
    echo "WARNING: Docker Compose not detected."
fi

# 3. Check psql
echo -n "Checking psql client... "
if command -v psql >/dev/null 2>&1; then
    PSQL_VER=$(psql --version | awk '{print $3}')
    echo "OK (psql $PSQL_VER)"
else
    echo "NOTE: psql not found on host PATH. You can use 'make psql' inside Docker."
fi

# 4. Check Python 3
echo -n "Checking Python 3... "
if command -v python3 >/dev/null 2>&1; then
    PY_VER=$(python3 --version | awk '{print $2}')
    echo "OK (Python $PY_VER)"
else
    echo "ERROR: Python 3 is required for query grading and mini-engine labs."
    EXIT_CODE=1
fi

# 5. Check Python dependencies
echo -n "Checking Python libraries... "
MISSING_PKGS=()
for pkg in psycopg tabulate pytest rich sqlparse; do
    if ! python3 -c "import $pkg" >/dev/null 2>&1; then
        MISSING_PKGS+=("$pkg")
    fi
done

if [ ${#MISSING_PKGS[@]} -eq 0 ]; then
    echo "OK (All core lab dependencies installed)"
else
    echo "NOTE: Missing Python packages: ${MISSING_PKGS[*]}. Run: pip install -r requirements.txt"
fi

echo "======================================================================"
if [ $EXIT_CODE -eq 0 ]; then
    echo "Status: Environment Ready! Start your database with: make up"
else
    echo "Status: Some requirements are missing or inactive."
fi
echo "======================================================================"
exit $EXIT_CODE
