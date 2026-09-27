#!/usr/bin/env bash
# ==============================================================================
# check-environment.sh - Diagnostic environment verification for Elasticsearch Lab
# ==============================================================================
set -euo pipefail

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}======================================================${NC}"
echo -e "${BLUE}  elasticsearch-from-scratch Environment Checker      ${NC}"
echo -e "${BLUE}======================================================${NC}"

# 1. Check Python
echo -n "Checking Python version (>= 3.11)... "
if command -v python3 &>/dev/null; then
    PY_VER=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
    PY_MAJOR=$(echo "$PY_VER" | cut -d. -f1)
    PY_MINOR=$(echo "$PY_VER" | cut -d. -f2)
    if [ "$PY_MAJOR" -ge 3 ] && [ "$PY_MINOR" -ge 11 ]; then
        echo -e "${GREEN}OK${NC} (Python $PY_VER)"
    else
        echo -e "${RED}FAILED${NC} (Python $PY_VER detected, >= 3.11 required)"
    fi
else
    echo -e "${RED}FAILED${NC} (python3 not found)"
fi

# 2. Check Docker
echo -n "Checking Docker... "
if command -v docker &>/dev/null; then
    if docker info &>/dev/null; then
        DOCKER_VER=$(docker --version | awk '{print $3}' | tr -d ',')
        echo -e "${GREEN}OK${NC} (Docker $DOCKER_VER)"
    else
        echo -e "${YELLOW}WARNING${NC} (Docker installed but daemon is not running)"
    fi
else
    echo -e "${RED}FAILED${NC} (docker not found)"
fi

# 3. Check Docker Compose
echo -n "Checking Docker Compose... "
if docker compose version &>/dev/null; then
    COMPOSE_VER=$(docker compose version --short)
    echo -e "${GREEN}OK${NC} (Docker Compose $COMPOSE_VER)"
else
    echo -e "${RED}FAILED${NC} (docker compose not available)"
fi

# 4. Check curl
echo -n "Checking curl... "
if command -v curl &>/dev/null; then
    CURL_VER=$(curl --version | head -n1 | awk '{print $2}')
    echo -e "${GREEN}OK${NC} (curl $CURL_VER)"
else
    echo -e "${RED}FAILED${NC} (curl not found)"
fi

# 5. Check Elasticsearch connectivity on port 9200
echo -n "Checking Elasticsearch service on localhost:9200... "
if curl -s http://localhost:9200 &>/dev/null; then
    ES_JSON=$(curl -s http://localhost:9200)
    ES_VER=$(echo "$ES_JSON" | grep -o '"number" : "[^"]*"' | head -n1 | cut -d'"' -f4 || echo "unknown")
    LUCENE_VER=$(echo "$ES_JSON" | grep -o '"lucene_version" : "[^"]*"' | head -n1 | cut -d'"' -f4 || echo "unknown")
    echo -e "${GREEN}ONLINE${NC} (Elasticsearch $ES_VER, Lucene $LUCENE_VER)"
else
    echo -e "${YELLOW}OFFLINE${NC} (Not running yet. Run 'make up' to start)"
fi

echo -e "${BLUE}======================================================${NC}"
echo -e "Environment check complete."
