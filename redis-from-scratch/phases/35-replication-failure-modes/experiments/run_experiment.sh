#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 35 Experiment: Replication Failure Modes: Backlog Overflow & Desync ==="
python3 phases/35-replication-failure-modes/code/repl_failure_modes.py
echo "✓ Phase 35 Experiment Complete."
