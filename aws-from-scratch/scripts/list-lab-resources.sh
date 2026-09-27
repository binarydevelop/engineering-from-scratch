#!/usr/bin/env bash
# ==============================================================================
# scripts/list-lab-resources.sh
# Discovers and reports all active AWS resources tagged with Project=aws-from-scratch.
# This script is strictly READ-ONLY. It never deletes resources.
# ==============================================================================

set -euo pipefail

BOLD="\033[1m"
GREEN="\033[0;32m"
YELLOW="\033[0;33m"
RED="\033[0;31m"
BLUE="\033[0;34m"
RESET="\033[0m"

TAG_KEY="Project"
TAG_VAL="aws-from-scratch"
REGION="${AWS_REGION:-${AWS_DEFAULT_REGION:-us-east-1}}"

echo -e "${BLUE}${BOLD}=====================================================${RESET}"
echo -e "${BLUE}${BOLD}      aws-from-scratch: Lab Resource Inventory       ${RESET}"
echo -e "${BLUE}${BOLD}=====================================================${RESET}"
echo -e "Target Region: ${BLUE}$REGION${RESET}"
echo -e "Filter Tag:    ${BLUE}$TAG_KEY=$TAG_VAL${RESET}"
echo ""

# Verify credentials exist before proceeding
if ! aws sts get-caller-identity >/dev/null 2>&1; then
    echo -e "${YELLOW}Notice: AWS credentials not configured. Skipping remote API discovery.${RESET}"
    echo "To test with live AWS, authenticate with: aws sso login"
    exit 0
fi

FOUND_COUNT=0

echo -e "${BOLD}Scanning for tagged lab infrastructure...${RESET}"
echo ""

# Method 1: AWS Resource Groups Tagging API (Fast global/regional tag search)
if aws resourcegroupstaggingapi get-resources --version >/dev/null 2>&1; then
    echo -n "Querying Resource Groups Tagging API... "
    TAGGED_ARNS=$(aws resourcegroupstaggingapi get-resources \
        --tag-filters "Key=$TAG_KEY,Values=$TAG_VAL" \
        --region "$REGION" \
        --query "ResourceTagMappingList[].ResourceARN" \
        --output text 2>/dev/null || true)
    
    if [ -n "$TAGGED_ARNS" ]; then
        echo -e "${RED}RESOURCES FOUND${RESET}"
        echo ""
        echo -e "${BOLD}Active Tagged Resources:${RESET}"
        for arn in $TAGGED_ARNS; do
            echo -e "  - ${YELLOW}$arn${RESET}"
            FOUND_COUNT=$((FOUND_COUNT + 1))
        done
    else
        echo -e "${GREEN}ZERO FOUND${RESET}"
    fi
fi

echo ""
echo -e "${BOLD}Direct Service Checks (${REGION}):${RESET}"

# 1. EC2 Instances
echo -n "  Checking EC2 instances... "
EC2_LIST=$(aws ec2 describe-instances \
    --region "$REGION" \
    --filters "Name=tag:$TAG_KEY,Values=$TAG_VAL" "Name=instance-state-name,Values=pending,running,stopping,stopped" \
    --query "Reservations[].Instances[].[InstanceId, State.Name, InstanceType]" \
    --output text 2>/dev/null || true)

if [ -n "$EC2_LIST" ]; then
    echo -e "${RED}FOUND${RESET}"
    echo "$EC2_LIST" | while read -r line; do
        echo -e "    ${YELLOW}$line${RESET}"
        FOUND_COUNT=$((FOUND_COUNT + 1))
    done
else
    echo -e "${GREEN}Clean${RESET}"
fi

# 2. VPCs
echo -n "  Checking VPCs... "
VPC_LIST=$(aws ec2 describe-vpcs \
    --region "$REGION" \
    --filters "Name=tag:$TAG_KEY,Values=$TAG_VAL" \
    --query "Vpcs[].[VpcId, CidrBlock]" \
    --output text 2>/dev/null || true)

if [ -n "$VPC_LIST" ]; then
    echo -e "${RED}FOUND${RESET}"
    echo "$VPC_LIST" | while read -r line; do
        echo -e "    ${YELLOW}$line${RESET}"
        FOUND_COUNT=$((FOUND_COUNT + 1))
    done
else
    echo -e "${GREEN}Clean${RESET}"
fi

# 3. S3 Buckets
echo -n "  Checking S3 buckets... "
S3_LIST=$(aws s3api list-buckets --query "Buckets[?starts_with(Name, 'aws-from-scratch')].Name" --output text 2>/dev/null || true)
if [ -n "$S3_LIST" ]; then
    echo -e "${RED}FOUND${RESET}"
    for b in $S3_LIST; do
        echo -e "    ${YELLOW}$b${RESET}"
        FOUND_COUNT=$((FOUND_COUNT + 1))
    done
else
    echo -e "${GREEN}Clean${RESET}"
fi

# 4. DynamoDB Tables
echo -n "  Checking DynamoDB tables... "
DDB_LIST=$(aws dynamodb list-tables --region "$REGION" --query "TableNames[?starts_with(@, 'aws-from-scratch')]" --output text 2>/dev/null || true)
if [ -n "$DDB_LIST" ]; then
    echo -e "${RED}FOUND${RESET}"
    for t in $DDB_LIST; do
        echo -e "    ${YELLOW}$t${RESET}"
        FOUND_COUNT=$((FOUND_COUNT + 1))
    done
else
    echo -e "${GREEN}Clean${RESET}"
fi

# 5. SQS Queues
echo -n "  Checking SQS queues... "
SQS_LIST=$(aws sqs list-queues --region "$REGION" --queue-name-prefix "aws-from-scratch" --query "QueueUrls[]" --output text 2>/dev/null || true)
if [ -n "$SQS_LIST" ]; then
    echo -e "${RED}FOUND${RESET}"
    for q in $SQS_LIST; do
        echo -e "    ${YELLOW}$q${RESET}"
        FOUND_COUNT=$((FOUND_COUNT + 1))
    done
else
    echo -e "${GREEN}Clean${RESET}"
fi

# 6. Lambda Functions
echo -n "  Checking Lambda functions... "
LAMBDA_LIST=$(aws lambda list-functions --region "$REGION" --query "Functions[?starts_with(FunctionName, 'aws-from-scratch')].FunctionName" --output text 2>/dev/null || true)
if [ -n "$LAMBDA_LIST" ]; then
    echo -e "${RED}FOUND${RESET}"
    for f in $LAMBDA_LIST; do
        echo -e "    ${YELLOW}$f${RESET}"
        FOUND_COUNT=$((FOUND_COUNT + 1))
    done
else
    echo -e "${GREEN}Clean${RESET}"
fi

echo ""
echo -e "${BOLD}--- Inventory Summary ---${RESET}"
if [ $FOUND_COUNT -eq 0 ]; then
    echo -e "${GREEN}${BOLD}✓ Zero active lab resources found. Account is clean!${RESET}"
    exit 0
else
    echo -e "${RED}${BOLD}⚠ Found $FOUND_COUNT active lab resource(s)!${RESET}"
    echo "Refer to the respective lesson's ## Cleanup section to terminate them and prevent ongoing charges."
    exit 2
fi
