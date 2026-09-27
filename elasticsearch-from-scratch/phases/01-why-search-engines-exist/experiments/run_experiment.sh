#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 01: Benchmarking Linear Document Scan ==="
python3 phases/01-why-search-engines-exist/code/linear_vs_index.py
