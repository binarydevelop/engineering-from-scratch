#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 02 Experiment: MiniKV In-Memory Store ==="
python3 phases/02-build-a-tiny-key-value-store/code/mini_kv.py
echo "✓ Phase 02 Experiment Complete."
