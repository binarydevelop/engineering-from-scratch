#!/usr/bin/env bash
# AI Systems From Scratch - Cleanup Script
set -euo pipefail

echo "Cleaning up temporary files, caches, and test artifacts..."

find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete 2>/dev/null || true
find . -type f -name "*.log" -delete 2>/dev/null || true
find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true

rm -rf checkpoints/ outputs/*.tmp 2>/dev/null || true

echo "Cleanup complete."
