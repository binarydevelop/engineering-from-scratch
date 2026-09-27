#!/usr/bin/env bash
# run-tests.sh: Master test suite validating simulations, benchmarks, capstones, and labs
set -euo pipefail

BOLD='\033[1m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BOLD}${BLUE}================================================================${NC}"
echo -e "${BOLD}${BLUE}   OPERATING SYSTEMS FROM SCRATCH: AUTOMATED TEST SUITE         ${NC}"
echo -e "${BOLD}${BLUE}================================================================${NC}"

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PASS_COUNT=0
FAIL_COUNT=0

run_test() {
    local name="$1"
    local cmd="$2"
    echo -n "  Testing: ${name}... "
    if eval "$cmd" >/dev/null 2>&1; then
        echo -e "${GREEN}PASS${NC}"
        PASS_COUNT=$((PASS_COUNT + 1))
    else
        echo -e "${RED}FAIL${NC}"
        FAIL_COUNT=$((FAIL_COUNT + 1))
    fi
}

echo -e "\n${BOLD}[1] Python Algorithmic Simulations:${NC}"
run_test "CPU Scheduler (FCFS, SJF, RR)" "python3 ${REPO_ROOT}/simulations/scheduler_sim.py"
run_test "Virtual Memory & TLB Translation" "python3 ${REPO_ROOT}/simulations/virtual_memory_sim.py"
run_test "Page Replacement & Belady Anomaly" "python3 ${REPO_ROOT}/simulations/page_replacement_sim.py"
run_test "Filesystem Crash & Journaling (WAL)" "python3 ${REPO_ROOT}/simulations/disk_consistency_sim.py"
run_test "Concurrency Race & Lock Ordering" "python3 ${REPO_ROOT}/simulations/concurrency_bank_sim.py"

echo -e "\n${BOLD}[2] Capstone Projects:${NC}"
run_test "Capstone 1: Mini-Shell Execution & Pipe" "echo 'echo test | tr a-z A-Z' | ${REPO_ROOT}/projects/01-tiny-shell/mini-shell"
run_test "Capstone 2: MLFQ Thread Scheduler" "python3 ${REPO_ROOT}/projects/02-scheduler-simulator/scheduler_sim.py"
run_test "Capstone 3: Virtual Memory & Page Eviction" "python3 ${REPO_ROOT}/projects/03-vm-simulator/vm_sim.py"
run_test "Capstone 4: Tiny Filesystem (TinyFS)" "python3 ${REPO_ROOT}/projects/04-tiny-fs/tiny_fs.py"
run_test "Capstone 5: HTTP Server Compilation" "test -f ${REPO_ROOT}/projects/05-event-http-server/http-server"
run_test "Capstone 6: Container Sandbox Launcher" "${REPO_ROOT}/projects/06-container-sandbox/container-launcher /bin/echo OK"

echo -e "\n${BOLD}[3] Systems Benchmarks:${NC}"
run_test "Process Context Switch (Pipe Roundtrip)" "${REPO_ROOT}/bin/context_switch"
run_test "I/O Buffering Throughput" "${REPO_ROOT}/bin/io_buffering"
run_test "CPU Cache Spatial Locality" "${REPO_ROOT}/bin/cache_locality"
run_test "Syscall vs Userspace Function Overhead" "${REPO_ROOT}/bin/syscall_overhead"

echo -e "\n${BOLD}[4] Broken Systems Solutions Verification:${NC}"
for s in "${REPO_ROOT}/bin"/solution-*; do
    name="$(basename "$s")"
    run_test "Solution: ${name}" "$s"
done

echo -e "\n${BOLD}${BLUE}================================================================${NC}"
echo -e "${BOLD}TEST SUMMARY: ${GREEN}${PASS_COUNT} Passed${NC}, ${RED}${FAIL_COUNT} Failed${NC}"
echo -e "${BOLD}${BLUE}================================================================${NC}\n"

if [[ $FAIL_COUNT -eq 0 ]]; then
    exit 0
else
    exit 1
fi
