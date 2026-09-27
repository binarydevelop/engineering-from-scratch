#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 32 Experiment: Latency Diagnosis: SLOWLOG, LATENCY DOCTOR, and Root Causes ==="
python3 phases/32-latency-diagnosis/code/latency_diagnosis.py
echo "✓ Phase 32 Experiment Complete."
