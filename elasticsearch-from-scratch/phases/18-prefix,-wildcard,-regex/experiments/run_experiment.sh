#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 18: Prefix vs Wildcard Benchmark ==="
python3 phases/18-prefix,-wildcard,-regex/code/18_prefix_wildcard.py
