#!/usr/bin/env bash
# check-environment.sh: Inspects the host platform for OS laboratory readiness
set -euo pipefail

BOLD='\033[1m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BOLD}${BLUE}================================================================${NC}"
echo -e "${BOLD}${BLUE}   OPERATING SYSTEMS FROM SCRATCH: ENVIRONMENT CHECKER           ${NC}"
echo -e "${BOLD}${BLUE}================================================================${NC}"

# 1. Detect Operating System and Kernel
OS_NAME="$(uname -s)"
KERNEL_VER="$(uname -r)"
ARCH="$(uname -m)"

echo -e "\n${BOLD}[1] Host Platform & Kernel:${NC}"
echo -e "  Operating System: ${GREEN}${OS_NAME}${NC}"
echo -e "  Kernel Release:   ${GREEN}${KERNEL_VER}${NC}"
echo -e "  Architecture:     ${GREEN}${ARCH}${NC}"

IS_LINUX=false
IS_WSL=false
IS_MACOS=false

if [[ "${OS_NAME}" == "Linux" ]]; then
    IS_LINUX=true
    if grep -qi "microsoft" /proc/version 2>/dev/null; then
        IS_WSL=true
        echo -e "  Platform Flavor:  ${GREEN}Windows Subsystem for Linux (WSL2)${NC}"
    else
        echo -e "  Platform Flavor:  ${GREEN}Native Linux${NC}"
    fi
elif [[ "${OS_NAME}" == "Darwin" ]]; then
    IS_MACOS=true
    echo -e "  Platform Flavor:  ${YELLOW}macOS Darwin (XNU Hybrid Kernel)${NC}"
    echo -e "  ${YELLOW}Note: POSIX labs run natively. Linux namespaces/cgroups/epoll require Docker or Lima VM.${NC}"
else
    echo -e "  Platform Flavor:  ${RED}Unknown / Untested (${OS_NAME})${NC}"
fi

# 2. Check Core Compilers and Runtimes
echo -e "\n${BOLD}[2] Compilers and Runtimes:${NC}"

check_cmd() {
    local cmd="$1"
    local required="$2"
    if command -v "$cmd" >/dev/null 2>&1; then
        local ver
        ver="$("$cmd" --version 2>&1 | head -n 1 || true)"
        if [[ -z "$ver" || "$ver" == *"illegal option"* || "$ver" == *"usage"* ]]; then
            ver="$("$cmd" -v 2>&1 | head -n 1 || true)"
        fi
        if [[ -z "$ver" || "$ver" == *"illegal option"* || "$ver" == *"usage"* ]]; then
            ver="Installed ($(command -v "$cmd"))"
        fi
        echo -e "  [x] ${GREEN}${cmd}${NC}: ${ver}"
        return 0
    else
        if [[ "$required" == "true" ]]; then
            echo -e "  [ ] ${RED}${cmd}${NC}: NOT FOUND (Required!)"
            return 1
        else
            echo -e "  [-] ${YELLOW}${cmd}${NC}: Not installed (Optional)"
            return 0
        fi
    fi
}

check_cmd "gcc" "false" || true
check_cmd "clang" "false" || true
check_cmd "make" "true"
check_cmd "python3" "true"

# 3. Check Diagnostic and Tracing Tools
echo -e "\n${BOLD}[3] Diagnostic & Inspection Utilities:${NC}"
check_cmd "strace" "false" || true
check_cmd "lsof" "false" || true
check_cmd "gdb" "false" || true
check_cmd "valgrind" "false" || true
check_cmd "ps" "true"
check_cmd "top" "true"

if [[ "$IS_LINUX" == "true" ]]; then
    check_cmd "ss" "false" || true
    check_cmd "ip" "false" || true
    check_cmd "perf" "false" || true
fi

# 4. Check Pseudo-Filesystems
echo -e "\n${BOLD}[4] Virtual Filesystems:${NC}"
if [[ -d "/proc" ]]; then
    echo -e "  [x] ${GREEN}/proc${NC}: Mounted and accessible"
else
    echo -e "  [ ] ${YELLOW}/proc${NC}: Not found (macOS uses Mach APIs and sysctl)"
fi

if [[ -d "/sys" ]]; then
    echo -e "  [x] ${GREEN}/sys${NC}: Mounted and accessible"
else
    echo -e "  [-] ${YELLOW}/sys${NC}: Not found"
fi

# 5. Summary & Guidance
echo -e "\n${BOLD}[5] Environment Readiness Summary:${NC}"
if [[ "$IS_LINUX" == "true" ]]; then
    echo -e "  ${GREEN}All 132 phases can run natively on this Linux system.${NC}"
elif [[ "$IS_MACOS" == "true" ]]; then
    echo -e "  ${GREEN}Ready for native POSIX C programming, threads, sockets, and Python simulations.${NC}"
    echo -e "  ${YELLOW}For Phases 70 (epoll), 95-102 (namespaces/cgroups), and 124 (container capstone),${NC}"
    echo -e "  ${YELLOW}please refer to docs/platform-setup.md to run inside Docker or Lima.${NC}"
fi

echo -e "\n${BOLD}${BLUE}Environment verification complete!${NC}\n"
exit 0
