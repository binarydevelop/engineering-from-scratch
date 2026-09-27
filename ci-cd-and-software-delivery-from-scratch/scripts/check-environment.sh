#!/usr/bin/env bash
# ==============================================================================
# Script: check-environment.sh
# Purpose: Preflight verification of local tooling, runtimes, and system state.
# Motto: Understand it. Build it. Test it. Package it. Verify it. Release it.
#        Deploy it. Observe it. Recover it. Automate it.
# ==============================================================================
set -euo pipefail

BOLD="\033[1m"
GREEN="\033[32m"
YELLOW="\033[33m"
RED="\033[31m"
RESET="\033[0m"

echo -e "${BOLD}======================================================================${RESET}"
echo -e "${BOLD} CI/CD and Software Delivery from Scratch — Environment Preflight${RESET}"
echo -e "${BOLD}======================================================================${RESET}"

ERRORS=0
WARNINGS=0

check_tool() {
    local tool_name="$1"
    local required="$2"
    local hint="$3"

    if command -v "$tool_name" >/dev/null 2>&1; then
        local version_output
        version_output=$("$tool_name" --version 2>&1 | head -n 1 || true)
        echo -e "  [${GREEN}FOUND${RESET}] ${BOLD}${tool_name}${RESET}: ${version_output}"
    else
        if [ "$required" = "true" ]; then
            echo -e "  [${RED}MISSING REQUIRED${RESET}] ${BOLD}${tool_name}${RESET}"
            echo -e "         ${YELLOW}Remediation: ${hint}${RESET}"
            ERRORS=$((ERRORS + 1))
        else
            echo -e "  [${YELLOW}OPTIONAL MISSING${RESET}] ${tool_name}"
            echo -e "         Note: ${hint}"
            WARNINGS=$((WARNINGS + 1))
        fi
    fi
}

echo -e "\n${BOLD}1. Checking Core Runtimes & Version Control:${RESET}"
check_tool "git" "true" "Install git via package manager (e.g. brew install git or apt-get install git)"
check_tool "python3" "true" "Install Python 3.10+ (tested through 3.14)"
check_tool "bash" "true" "Bash shell required (POSIX compliant)"

echo -e "\n${BOLD}2. Checking Packaging & System Utilities:${RESET}"
check_tool "tar" "true" "Standard archiving utility required for artifact packaging"
if command -v sha256sum >/dev/null 2>&1; then
    echo -e "  [${GREEN}FOUND${RESET}] ${BOLD}sha256sum${RESET}: Available for cryptographic artifact hashing"
elif command -v shasum >/dev/null 2>&1; then
    echo -e "  [${GREEN}FOUND${RESET}] ${BOLD}shasum (macOS)${RESET}: Available for cryptographic artifact hashing"
else
    echo -e "  [${RED}MISSING REQUIRED${RESET}] sha256sum/shasum"
    echo -e "         ${YELLOW}Remediation: Install coreutils (brew install coreutils)${RESET}"
    ERRORS=$((ERRORS + 1))
fi

echo -e "\n${BOLD}3. Checking Optional Container & Cloud Delivery Tools:${RESET}"
check_tool "docker" "false" "Docker Engine is optional for container labs (local runner works standalone)"
check_tool "kubectl" "false" "Kubectl is optional for Kubernetes GitOps labs"
check_tool "helm" "false" "Helm is optional for Kubernetes package management"
check_tool "cosign" "false" "Cosign is optional for Sigstore image signing labs"

echo -e "\n${BOLD}4. Checking Git Repository State:${RESET}"
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    COMMIT_SHA=$(git rev-parse HEAD 2>/dev/null || echo "INITIAL-COMMIT")
    BRANCH_NAME=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "unnamed")
    echo -e "  [${GREEN}OK${RESET}] Inside Git Repository"
    echo -e "       Current Commit: ${BOLD}${COMMIT_SHA}${RESET}"
    echo -e "       Current Branch: ${BOLD}${BRANCH_NAME}${RESET}"
else
    echo -e "  [${RED}NOT IN GIT REPO${RESET}] Run 'git init' in the project directory"
    ERRORS=$((ERRORS + 1))
fi

echo -e "\n----------------------------------------------------------------------"
if [ "$ERRORS" -eq 0 ]; then
    echo -e "${GREEN}${BOLD}✓ Preflight passed! Your environment is ready.${RESET}"
    if [ "$WARNINGS" -gt 0 ]; then
        echo -e "${YELLOW}  (${WARNINGS} optional tools missing; core simulators will run standalone.)${RESET}"
    fi
    exit 0
else
    echo -e "${RED}${BOLD}✗ Preflight failed with ${ERRORS} error(s). Please address required tools above.${RESET}"
    exit 1
fi
