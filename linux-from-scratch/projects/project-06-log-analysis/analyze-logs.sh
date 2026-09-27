#!/usr/bin/env bash
# High-Performance Log Analysis Pipeline
set -euo pipefail

LOG_FILE="${1:-projects/project-06-log-analysis/sample-access.log}"

if [ ! -f "$LOG_FILE" ]; then
    echo "ERROR: Log file $LOG_FILE not found." >&2
    exit 1
fi

echo "=========================================================="
echo "          LOG STREAM AUDIT REPORT : $LOG_FILE             "
echo "=========================================================="

echo ""
echo "--- [1] TOP 5 CLIENT IP ADDRESSES ---"
awk '{print $1}' "$LOG_FILE" | sort | uniq -c | sort -nr | head -5

echo ""
echo "--- [2] HTTP RESPONSE CODE DISTRIBUTION ---"
awk '{print $9}' "$LOG_FILE" | sort | uniq -c | sort -nr

echo ""
echo "--- [3] TOP REQUESTED ENDPOINTS ---"
awk '{print $7}' "$LOG_FILE" | sort | uniq -c | sort -nr | head -5

echo ""
echo "--- [4] HTTP 5xx SERVER ERRORS ---"
awk '$9 ~ /^5/ {print $1, $4, $7, $9}' "$LOG_FILE" || echo "Zero 5xx errors detected."

echo ""
echo "--- [5] POTENTIAL BRUTE FORCE ATTACKERS (Repeated 401s) ---"
awk '$9 == 401 {print $1}' "$LOG_FILE" | sort | uniq -c | awk '$1 >= 3 {print "IP: " $2 " (Failures: " $1 ")"}'
echo "=========================================================="
