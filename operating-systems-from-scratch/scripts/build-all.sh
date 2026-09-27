#!/usr/bin/env bash
# build-all.sh: Compiles all C systems programs, benchmarks, capstones, and labs
set -euo pipefail

BOLD='\033[1m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BOLD}${BLUE}================================================================${NC}"
echo -e "${BOLD}${BLUE}   OPERATING SYSTEMS FROM SCRATCH: COMPILING ALL TARGETS        ${NC}"
echo -e "${BOLD}${BLUE}================================================================${NC}"

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
mkdir -p "${REPO_ROOT}/bin"

CC="${CC:-gcc}"
CFLAGS="-Wall -Wextra -pedantic -std=c11 -pthread -O2"

compile_binary() {
    local src="$1"
    local out="$2"
    echo -n "  Compiling $(basename "$src")... "
    if $CC $CFLAGS "$src" -o "$out"; then
        echo -e "${GREEN}OK${NC}"
    else
        echo -e "${RED}FAILED${NC}"
        return 1
    fi
}

echo -e "\n${BOLD}[1] Compiling Benchmarks:${NC}"
for b in "${REPO_ROOT}/benchmarks"/*.c; do
    name="$(basename "$b" .c)"
    compile_binary "$b" "${REPO_ROOT}/bin/${name}"
done

echo -e "\n${BOLD}[2] Compiling Capstone Projects:${NC}"
make -C "${REPO_ROOT}/projects/01-tiny-shell" >/dev/null
echo -e "  [x] ${GREEN}Capstone 1 (mini-shell)${NC}"

make -C "${REPO_ROOT}/projects/05-event-http-server" >/dev/null
echo -e "  [x] ${GREEN}Capstone 5 (http-server)${NC}"

make -C "${REPO_ROOT}/projects/06-container-sandbox" >/dev/null
echo -e "  [x] ${GREEN}Capstone 6 (container-launcher)${NC}"

echo -e "\n${BOLD}[3] Compiling Broken Systems Solutions:${NC}"
for s in "${REPO_ROOT}/solutions/broken-systems"/*.c; do
    name="$(basename "$s" .c)"
    compile_binary "$s" "${REPO_ROOT}/bin/${name}"
done

echo -e "\n${BOLD}${GREEN}All binaries compiled successfully! Output directory: bin/${NC}\n"
