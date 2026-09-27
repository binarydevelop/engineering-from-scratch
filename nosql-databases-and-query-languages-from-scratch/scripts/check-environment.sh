#!/usr/bin/env bash
set -euo pipefail

echo "======================================================================"
echo "  NoSQL Databases & Query Languages From Scratch - Environment Check   "
echo "======================================================================"

PASS=0
FAIL=0

check_cmd() {
    local cmd="$1"
    local name="$2"
    if command -v "$cmd" >/dev/null 2>&1; then
        local version
        version=$("$cmd" --version 2>&1 | head -n 1 || true)
        echo " [OK] $name: $version"
        PASS=$((PASS + 1))
    else
        echo " [WARN] $name ($cmd) not found on PATH (will use Docker or simulation mode)"
    fi
}

check_port() {
    local port="$1"
    local service="$2"
    if nc -z localhost "$port" 2>/dev/null || (echo > /dev/tcp/localhost/"$port") 2>/dev/null; then
        echo " [LIVE] $service is running on port $port"
    else
        echo " [IDLE] $service is not currently listening on port $port"
    fi
}

echo ""
echo "--- Host Runtimes ---"
check_cmd "python3" "Python 3 Runtime"
check_cmd "docker" "Docker Engine"
check_cmd "docker-compose" "Docker Compose" || check_cmd "docker" "Docker Compose Plugin"
check_cmd "mongosh" "MongoDB Shell"
check_cmd "redis-cli" "Redis CLI"
check_cmd "curl" "cURL Client"

echo ""
echo "--- Container / Database Ports Check ---"
check_port 27017 "MongoDB (MQL)"
check_port 9042  "Apache Cassandra (CQL)"
check_port 8000  "DynamoDB Local (PartiQL/Native)"
check_port 6379  "Redis (In-Memory/Commands)"
check_port 7474  "Neo4j HTTP (Browser UI)"
check_port 7687  "Neo4j Bolt Protocol (Cypher)"
check_port 9200  "Elasticsearch (Query DSL)"

echo ""
echo "Environment check complete. You can start local database labs using: ./scripts/start-lab.sh <profile>"
