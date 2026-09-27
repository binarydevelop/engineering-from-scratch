#!/usr/bin/env bash
# ==============================================================================
# scripts/check-environment.sh
# Verifies system requirements, tool versions, and local environment.
# ==============================================================================

set -euo pipefail

BOLD="\033[1m"
GREEN="\033[0;32m"
YELLOW="\033[0;33m"
RED="\033[0;31m"
BLUE="\033[0;34m"
RESET="\033[0m"

echo -e "${BLUE}${BOLD}=====================================================${RESET}"
echo -e "${BLUE}${BOLD}   aws-from-scratch: Environment Verification Check  ${RESET}"
echo -e "${BLUE}${BOLD}=====================================================${RESET}"
echo ""

ERRORS=0
WARNINGS=0

check_tool() {
    local tool="$1"
    local min_ver="$2"
    local check_cmd="$3"

    echo -n "Checking $tool... "
    if command -v "$tool" >/dev/null 2>&1; then
        local version
        version=$(eval "$check_cmd" 2>&1 | head -n 1)
        echo -e "${GREEN}FOUND${RESET} ($version)"
    else
        echo -e "${RED}MISSING${RESET} (Required: $min_ver)"
        ERRORS=$((ERRORS + 1))
    fi
}

check_optional() {
    local tool="$1"
    local purpose="$2"

    echo -n "Checking optional tool: $tool ($purpose)... "
    if command -v "$tool" >/dev/null 2>&1; then
        echo -e "${GREEN}INSTALLED${RESET}"
    else
        echo -e "${YELLOW}NOT FOUND${RESET} (Optional)"
        WARNINGS=$((WARNINGS + 1))
    fi
}

# 1. Python 3.12+
check_tool "python3" ">= 3.12" "python3 --version"

# 2. AWS CLI v2
check_tool "aws" "AWS CLI v2" "aws --version"

# 3. Docker
check_tool "docker" "Docker Engine 24+" "docker --version"

# 4. Git
check_tool "git" "Git 2.x" "git --version"

# 5. curl
check_tool "curl" "curl 7+" "curl --version"

# 6. Optional utilities
check_optional "jq" "JSON parsing for CLI output"
check_optional "terraform" "Reference Infrastructure as Code (Phases 57-60)"

echo ""
echo -e "${BOLD}--- Python Virtual Environment Check ---${RESET}"
if [ -n "${VIRTUAL_ENV:-}" ]; then
    echo -e "${GREEN}Active virtual environment detected:${RESET} $VIRTUAL_ENV"
else
    echo -e "${YELLOW}Warning: No virtual environment currently active.${RESET}"
    echo "Tip: Run 'python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt'"
    WARNINGS=$((WARNINGS + 1))
fi

echo ""
echo -e "${BOLD}--- Verification Summary ---${RESET}"
if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}${BOLD}✓ Core environment is ready for aws-from-scratch!${RESET}"
    if [ $WARNINGS -gt 0 ]; then
        echo -e "${YELLOW}(Optional tools or virtual environment recommendations were noted above.)${RESET}"
    fi
    exit 0
else
    echo -e "${RED}${BOLD}✗ Missing $ERRORS required tool(s). Please install them before proceeding.${RESET}"
    exit 1
fi
