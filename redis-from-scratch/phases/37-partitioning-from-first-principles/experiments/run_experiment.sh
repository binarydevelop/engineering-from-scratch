#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 37 Experiment: Partitioning From First Principles: Modulo vs. Hash Slots ==="
python3 phases/37-partitioning-from-first-principles/code/partitioning_modulo.py
echo "✓ Phase 37 Experiment Complete."
