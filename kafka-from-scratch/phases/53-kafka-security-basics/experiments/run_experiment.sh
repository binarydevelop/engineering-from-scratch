#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 53 Experiment: Inspecting Kafka Security Protocols ==="
cd "$(dirname "$0")/.."
../../.venv/bin/python3 code/security_config_inspector.py
