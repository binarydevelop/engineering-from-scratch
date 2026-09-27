#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 44 Experiment: Real Application: Distributed Rate Limiter ==="
python3 phases/44-real-application-rate-limiter/code/rate_limiter_app.py
echo "✓ Phase 44 Experiment Complete."
