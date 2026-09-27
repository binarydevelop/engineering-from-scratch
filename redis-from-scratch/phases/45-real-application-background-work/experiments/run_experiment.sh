#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 45 Experiment: Real Application: Durable Background Worker Pipeline ==="
python3 phases/45-real-application-background-work/code/task_pipeline_app.py
echo "✓ Phase 45 Experiment Complete."
