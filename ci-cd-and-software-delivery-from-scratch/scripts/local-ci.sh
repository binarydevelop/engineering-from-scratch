#!/usr/bin/env bash
# ==============================================================================
# Script: local-ci.sh
# Purpose: Standalone, platform-independent Local CI pipeline.
# Motto: Understand it. Build it. Test it. Package it. Verify it. Release it.
#        Deploy it. Observe it. Recover it. Automate it.
# Stage: Phase 05, 06, 11, 206
# ==============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

BOLD="\033[1m"
GREEN="\033[32m"
RED="\033[31m"
BLUE="\033[34m"
RESET="\033[0m"

echo -e "${BOLD}======================================================================${RESET}"
echo -e "${BOLD}  LOCAL CI PIPELINE HARNESS — FROM SCRATCH${RESET}"
echo -e "${BOLD}======================================================================${RESET}"

TOTAL_START=$(date +%s)
FAILED_STAGE=""

run_stage() {
    local stage_name="$1"
    local command="$2"
    local stage_start
    stage_start=$(date +%s)

    echo -e "\n${BLUE}▶ [STAGE] ${stage_name}${RESET}"
    if eval "$command"; then
        local stage_end
        stage_end=$(date +%s)
        local stage_duration=$((stage_end - stage_start))
        echo -e "${GREEN}✓ [STAGE PASSED] ${stage_name} (${stage_duration}s)${RESET}"
    else
        local exit_code=$?
        local stage_end
        stage_end=$(date +%s)
        local stage_duration=$((stage_end - stage_start))
        echo -e "${RED}✗ [STAGE FAILED] ${stage_name} with exit code ${exit_code} (${stage_duration}s)${RESET}" >&2
        FAILED_STAGE="${stage_name}"
        return $exit_code
    fi
}

# Stage 1: Preflight Verification
run_stage "Environment Preflight" "${SCRIPT_DIR}/check-environment.sh"

# Stage 2: Static Verification & Syntax Compilation
run_stage "Static Syntax & Bytecode Compilation" "python3 -m py_compile ${ROOT_DIR}/sample-apps/delivery-service/app.py"

# Stage 3: Secret Scanning (Phase 41)
run_stage "Secret Scanner" "python3 ${ROOT_DIR}/security-labs/secret_leak_scanner.py --scan-dir ${ROOT_DIR}/sample-apps"

# Stage 4: Test Suite (Unit, Integration, Contract, Smoke)
run_stage "Automated Test Matrix" "${SCRIPT_DIR}/test.sh"

# Stage 5: Deterministic Build
run_stage "Deterministic Build" "${SCRIPT_DIR}/build.sh"

# Stage 6: Immutable Packaging & Checksums
run_stage "Artifact Packaging & Checksum Generation" "${SCRIPT_DIR}/package.sh"

TOTAL_END=$(date +%s)
TOTAL_DURATION=$((TOTAL_END - TOTAL_START))

echo -e "\n======================================================================"
echo -e "${GREEN}${BOLD}✓ LOCAL CI PIPELINE COMPLETED SUCCESSFULLY in ${TOTAL_DURATION}s!${RESET}"
echo -e "======================================================================"
