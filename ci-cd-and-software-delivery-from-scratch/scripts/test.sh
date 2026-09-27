#!/usr/bin/env bash
# ==============================================================================
# Script: test.sh
# Purpose: Execute unit, integration, contract, and smoke test suites.
# Stage: Phase 04, 24, 25, 33, 95
# ==============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
APP_DIR="${ROOT_DIR}/sample-apps/delivery-service"

echo "========================================================================"
echo " Running Automated Test Pipeline"
echo " Target: delivery-service"
echo "========================================================================"

FAILED=0
START_TIME=$(date +%s)

run_suite() {
    local suite_name="$1"
    local test_script="$2"
    echo -e "\n--- [Running ${suite_name}] ---"
    if python3 "${test_script}"; then
        echo "✓ ${suite_name}: PASSED"
    else
        echo "✗ ${suite_name}: FAILED" >&2
        FAILED=$((FAILED + 1))
    fi
}

# 1. Unit Tests (Phase 24 - Fast feedback)
run_suite "Unit Tests" "${APP_DIR}/tests/unit/test_orders.py"

# 2. Integration Tests (Phase 25 - Real database & migrations)
run_suite "Integration Tests" "${APP_DIR}/tests/integration/test_db.py"

# 3. Contract Tests (Phase 33 - API schema compatibility)
run_suite "Contract Tests" "${APP_DIR}/tests/contract/test_api_contract.py"

# 4. Smoke Tests (Phase 95 - Live health checks)
run_suite "Smoke Tests" "${APP_DIR}/tests/smoke/test_smoke.py"

END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))

echo "========================================================================"
if [ "$FAILED" -eq 0 ]; then
    echo "✓ All test suites passed successfully in ${DURATION}s."
    exit 0
else
    echo "✗ Test pipeline failed with ${FAILED} suite error(s) in ${DURATION}s." >&2
    exit 1
fi
