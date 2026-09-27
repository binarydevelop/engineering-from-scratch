#!/usr/bin/env bash
# ==============================================================================
# check-environment.sh
# Validates host networking tools, kernel capabilities, and runtime environments
# ==============================================================================

set -euo pipefail

BOLD="\033[1m"
GREEN="\033[32m"
YELLOW="\033[33m"
RED="\033[31m"
RESET="\033[0m"

echo -e "${BOLD}================================================================${RESET}"
echo -e "${BOLD}   computer-networking-from-scratch Environment Checker        ${RESET}"
echo -e "${BOLD}================================================================${RESET}"

OS="$(uname -s)"
echo -e "Operating System: ${BOLD}${OS}${RESET} ($(uname -m))"

# 1. Check Python
echo -n "Checking Python 3... "
if command -v python3 >/dev/null 2>&1; then
    PY_VER=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")')
    echo -e "${GREEN}Found Python ${PY_VER}${RESET}"
else
    echo -e "${RED}MISSING! Python 3.10+ is required.${RESET}"
fi

# 2. Check C Compiler
echo -n "Checking C Compiler (gcc/clang)... "
if command -v gcc >/dev/null 2>&1; then
    echo -e "${GREEN}Found gcc ($(gcc --version | head -n1))${RESET}"
elif command -v clang >/dev/null 2>&1; then
    echo -e "${GREEN}Found clang ($(clang --version | head -n1))${RESET}"
else
    echo -e "${YELLOW}No C compiler found (optional for C socket track).${RESET}"
fi

# 3. Check Core CLI Networking Tools
TOOLS=("curl" "ping" "tcpdump" "nc")
for tool in "${TOOLS[@]}"; do
    echo -n "Checking ${tool}... "
    if command -v "$tool" >/dev/null 2>&1; then
        echo -e "${GREEN}Available${RESET}"
    else
        echo -e "${YELLOW}Missing (${tool})${RESET}"
    fi
done

# DNS tool
echo -n "Checking DNS lookup (dig / getent)... "
if command -v dig >/dev/null 2>&1; then
    echo -e "${GREEN}Found dig${RESET}"
elif command -v getent >/dev/null 2>&1; then
    echo -e "${GREEN}Found getent${RESET}"
else
    echo -e "${YELLOW}Neither dig nor getent found.${RESET}"
fi

# 4. Linux-Specific Networking Primitives
if [ "$OS" = "Linux" ]; then
    echo -e "\n${BOLD}Linux Kernel & Networking Stack Inspection:${RESET}"
    
    echo -n "Checking iproute2 ('ip')... "
    if command -v ip >/dev/null 2>&1; then
        echo -e "${GREEN}Available${RESET}"
    else
        echo -e "${RED}Missing 'ip' command (apt install iproute2)${RESET}"
    fi

    echo -n "Checking socket stats ('ss')... "
    if command -v ss >/dev/null 2>&1; then
        echo -e "${GREEN}Available${RESET}"
    else
        echo -e "${RED}Missing 'ss' command (apt install iproute2)${RESET}"
    fi

    echo -n "Checking Network Namespaces ('ip netns')... "
    if ip netns >/dev/null 2>&1; then
        echo -e "${GREEN}Supported${RESET}"
    else
        echo -e "${YELLOW}Requires root or CAP_NET_ADMIN${RESET}"
    fi

    echo -n "Checking Firewall Tooling (nftables / iptables)... "
    if command -v nft >/dev/null 2>&1; then
        echo -e "${GREEN}Found nftables${RESET}"
    elif command -v iptables >/dev/null 2>&1; then
        echo -e "${GREEN}Found iptables${RESET}"
    else
        echo -e "${YELLOW}Neither nftables nor iptables found${RESET}"
    fi
else
    echo -e "\n${YELLOW}Note: Running on ${OS}.${RESET}"
    echo -e "Python simulators, socket servers/clients, and benchmarks run natively on macOS."
    echo -e "Linux network namespace labs ('ip netns', 'veth') can be executed inside Docker:"
    echo -e "  Run: ${BOLD}make docker-lab${RESET} or ${BOLD}./scripts/run-docker-lab.sh${RESET}"
fi

# 5. Check Docker
echo -n "Checking Docker daemon... "
if command -v docker >/dev/null 2>&1; then
    if docker info >/dev/null 2>&1; then
        echo -e "${GREEN}Docker daemon is active${RESET}"
    else
        echo -e "${YELLOW}Docker installed but daemon is not running${RESET}"
    fi
else
    echo -e "${YELLOW}Docker not installed (optional for containerized Linux lab)${RESET}"
fi

echo -e "\n${BOLD}Environment check completed.${RESET}"
