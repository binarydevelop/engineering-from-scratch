#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 45 Experiment: Demonstrating the Claim-Check Pattern ==="
cd "$(dirname "$0")/.."
../../.venv/bin/python3 code/claim_check_pattern.py
