#!/usr/bin/env bash
# scripts/clean_labs.sh
# Safely tears down containers, networks, and volumes created during docker-from-scratch lessons.

set -eo pipefail

echo "Cleaning up docker-from-scratch lab containers, networks, and volumes..."

# Stop and remove containers labeled or prefixed with dfs- or lesson names
CONTAINERS=$(docker ps -a --filter "name=dfs-" --format "{{.ID}}" 2>/dev/null || true)
if [ -n "$CONTAINERS" ]; then
    echo "Stopping and removing lab containers..."
    docker rm -f $CONTAINERS 2>/dev/null || true
fi

# Remove lab networks
NETWORKS=$(docker network ls --filter "name=dfs-" --format "{{.ID}}" 2>/dev/null || true)
if [ -n "$NETWORKS" ]; then
    echo "Removing lab networks..."
    docker network rm $NETWORKS 2>/dev/null || true
fi

# Remove lab volumes
VOLUMES=$(docker volume ls --filter "name=dfs-" --format "{{.Name}}" 2>/dev/null || true)
if [ -n "$VOLUMES" ]; then
    echo "Removing lab volumes..."
    docker volume rm $VOLUMES 2>/dev/null || true
fi

echo "Lab cleanup complete."
