#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 40 Experiment: Redis Security Basics: Protected Mode, ACLs, and TLS ==="
python3 phases/40-redis-security-basics/code/redis_security.py
echo "✓ Phase 40 Experiment Complete."
