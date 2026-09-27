#!/usr/bin/env bash
# ==============================================================================
# scripts/check-aws-identity.sh
# Verifies active AWS credentials, identifies the calling principal,
# and enforces the zero-root security protocol.
# ==============================================================================

set -euo pipefail

BOLD="\033[1m"
GREEN="\033[0;32m"
YELLOW="\033[0;33m"
RED="\033[0;31m"
BLUE="\033[0;34m"
RESET="\033[0m"

echo -e "${BLUE}${BOLD}=====================================================${RESET}"
echo -e "${BLUE}${BOLD}      aws-from-scratch: AWS Identity Inspector       ${RESET}"
echo -e "${BLUE}${BOLD}=====================================================${RESET}"
echo ""

# Check if AWS CLI is installed
if ! command -v aws >/dev/null 2>&1; then
    echo -e "${RED}Error: 'aws' CLI is not installed or not in PATH.${RESET}"
    exit 1
fi

echo -n "Interrogating AWS Security Token Service (STS)... "

# Attempt sts get-caller-identity
IDENTITY_JSON=$(aws sts get-caller-identity --output json 2>&1 || true)

if echo "$IDENTITY_JSON" | grep -q "Unable to locate credentials\|NoCredentials"; then
    echo -e "${YELLOW}NO CREDENTIALS CONFIGURED${RESET}"
    echo ""
    echo -e "${BOLD}No active AWS credentials detected.${RESET}"
    echo "To configure credentials safely for learning labs:"
    echo "  1. If using IAM Identity Center (SSO):"
    echo "     aws configure sso"
    echo "     aws sso login --profile <profile-name>"
    echo "  2. If using temporary session tokens:"
    echo "     export AWS_ACCESS_KEY_ID=ASIA..."
    echo "     export AWS_SECRET_ACCESS_KEY=..."
    echo "     export AWS_SESSION_TOKEN=..."
    echo "  3. DO NOT use root user credentials or create permanent admin access keys."
    echo ""
    echo -e "${BLUE}Note:${RESET} Local simulation labs (Phases 00, 03, 05, 22, 33, 81) can run without AWS credentials."
    exit 0
fi

if echo "$IDENTITY_JSON" | grep -q "error"; then
    echo -e "${RED}ERROR${RESET}"
    echo -e "${RED}STS call failed with output:${RESET}"
    echo "$IDENTITY_JSON"
    exit 1
fi

echo -e "${GREEN}AUTHENTICATED${RESET}"
echo ""

# Extract identity properties
ACCOUNT=$(echo "$IDENTITY_JSON" | grep -o '"Account": "[^"]*' | cut -d'"' -f4)
ARN=$(echo "$IDENTITY_JSON" | grep -o '"Arn": "[^"]*' | cut -d'"' -f4)
USER_ID=$(echo "$IDENTITY_JSON" | grep -o '"UserId": "[^"]*' | cut -d'"' -f4)

echo -e "${BOLD}Current Active Identity:${RESET}"
echo -e "  Account ID: ${BLUE}$ACCOUNT${RESET}"
echo -e "  Caller ARN: ${BLUE}$ARN${RESET}"
echo -e "  User ID:    ${BLUE}$USER_ID${RESET}"
echo ""

# CRITICAL SECURITY CHECK: Root Account Detection
if echo "$ARN" | grep -q ":root$"; then
    echo -e "${RED}${BOLD}!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!${RESET}"
    echo -e "${RED}${BOLD}CRITICAL SECURITY WARNING: YOU ARE RUNNING AS ROOT!       ${RESET}"
    echo -e "${RED}${BOLD}!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!${RESET}"
    echo -e "${RED}You are currently authenticated as the AWS account root user.${RESET}"
    echo -e "${RED}This violates Rule 0 of the AWS Security Protocol.${RESET}"
    echo ""
    echo "Actions required before running live infrastructure labs:"
    echo "  1. Log into the AWS Console as root."
    echo "  2. Enable MFA on the root account."
    echo "  3. Delete any root access keys."
    echo "  4. Create an IAM Identity Center user or a dedicated IAM Lab Role with least privilege."
    echo "  5. Switch to temporary credentials via 'aws sso login' or 'aws sts assume-role'."
    echo ""
    exit 1
fi

# Check for temporary credentials (assumed-role)
if echo "$ARN" | grep -q ":assumed-role/"; then
    echo -e "${GREEN}${BOLD}✓ Security Check Passed:${RESET} Using temporary assumed-role credentials."
elif echo "$ARN" | grep -q ":user/"; then
    echo -e "${YELLOW}${BOLD}! Note:${RESET} Using IAM User credentials. Ensure MFA is enabled and permissions follow least-privilege."
else
    echo -e "${GREEN}Principal type:${RESET} $ARN"
fi

echo ""
echo -e "${GREEN}Identity check complete.${RESET}"
exit 0
