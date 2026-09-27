#!/usr/bin/env bash
# Zombie Process Auditor
# Identifies processes in state 'Z' (zombies) and finds their neglectful parents
set -euo pipefail

echo "[*] Scanning process table for zombie processes (State: Z)..."

ZOMBIES=$(ps -eo pid,ppid,stat,comm | awk '$3 ~ /Z/ {print $1, $2, $4}')

if [ -z "$ZOMBIES" ]; then
    echo "[✓] Zero zombie processes detected. Process table healthy."
    exit 0
fi

echo "WARNING: Zombie processes detected!"
echo "PID   PPID  COMMAND"
echo "-------------------"
echo "$ZOMBIES"
echo ""
echo "--- Root Cause Analysis ---"
echo "A zombie process has exited, but its parent has not called wait() or waitpid() to reap its exit status."
echo "Zombies consume no CPU or RAM, but they leak process table slots (PIDs)."
echo "Remediation: You cannot kill a zombie with SIGKILL (it is already dead!). You must restart or signal the PARENT process (PPID)."
