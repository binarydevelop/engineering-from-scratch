#!/usr/bin/env bash
# ==============================================================================
# Script: rollback.sh
# Purpose: Execute automated rollback with database compatibility verification.
# Stage: Phase 104, 105, 106, 107
# ==============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

TARGET_ENV="${1:-staging}"
TARGET_DIGEST="${2:-prev-known-good}"

START_RECOVERY=$(date +%s)

echo "========================================================================"
echo " Executing Deployment Rollback"
echo " Target Environment : ${TARGET_ENV}"
echo " Target Digest      : ${TARGET_DIGEST}"
echo "========================================================================"

# 1. Rollback Feasibility Check: Database Schema Verification (Phase 106)
echo "Checking database backward compatibility..."
# Verify that running old code on current DB won't crash
python3 -c "
import sqlite3, sys
conn = sqlite3.connect('${ROOT_DIR}/sample-apps/delivery-service/delivery.db')
cur = conn.cursor()
try:
    cur.execute('SELECT id, customer_email, amount_cents FROM orders LIMIT 1')
    print('  ✓ Database schema remains compatible with prior application code.')
except Exception as e:
    print(f'  ✗ IRREVERSIBLE SCHEMA ERROR: Cannot rollback safely! Detail: {e}', file=sys.stderr)
    sys.exit(1)
"

# 2. Shift Traffic Routing Back (Phase 104)
echo "Shifting 100% traffic back to previous stable release..."
python3 "${ROOT_DIR}/deployment-labs/deploy_simulator.py" \
    --strategy blue-green \
    --action rollback \
    --target-env "${TARGET_ENV}"

END_RECOVERY=$(date +%s)
MTTR=$((END_RECOVERY - START_RECOVERY))

echo "========================================================================"
echo "✓ Rollback completed successfully in ${MTTR}s (Mean Time To Recovery)."
echo "========================================================================"
