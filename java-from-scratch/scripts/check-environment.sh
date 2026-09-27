#!/usr/bin/env bash
# ==============================================================================
# java-from-scratch Environment Checker
# Verifies JDK 21+ LTS, javac, javap, jcmd, jshell, Maven, and OS capabilities
# ==============================================================================

set -euo pipefail

BOLD="\033[1m"
GREEN="\033[0;32m"
RED="\033[0;31m"
YELLOW="\033[0;33m"
BLUE="\033[0;34m"
RESET="\033[0m"

echo -e "${BOLD}${BLUE}======================================================${RESET}"
echo -e "${BOLD}${BLUE}  java-from-scratch: Environment Verification Check  ${RESET}"
echo -e "${BOLD}${BLUE}======================================================${RESET}\n"

ERRORS=0

check_command() {
    local cmd="$1"
    local desc="$2"
    if command -v "$cmd" >/dev/null 2>&1; then
        local location
        location=$(command -v "$cmd")
        echo -e " [${GREEN}OK${RESET}] ${BOLD}$cmd${RESET} found ($desc): $location"
    else
        echo -e " [${RED}FAIL${RESET}] ${BOLD}$cmd${RESET} missing ($desc)"
        ERRORS=$((ERRORS + 1))
    fi
}

echo -e "${BOLD}Checking core JDK CLI utilities:${RESET}"
check_command "java" "Java Runtime Launcher"
check_command "javac" "Java Compiler"
check_command "javap" "Java Classfile Disassembler"
check_command "jcmd" "JVM Diagnostic Command Utility"
check_command "jshell" "Java Interactive Read-Eval-Print Loop"
check_command "jar" "Java Archive Tool"
check_command "mvn" "Apache Maven Build System"
check_command "git" "Version Control"

echo ""
echo -e "${BOLD}Verifying Java Version Constraints (Target: Java 21+ LTS):${RESET}"
if command -v java >/dev/null 2>&1; then
    JAVA_RAW_VERSION=$(java -version 2>&1 | head -n 1)
    echo -e " Runtime: $JAVA_RAW_VERSION"
    
    # Extract major version number
    JAVA_MAJOR=$(java -version 2>&1 | head -n 1 | awk -F '"' '{print $2}' | cut -d'.' -f1)
    if [ "$JAVA_MAJOR" -ge 21 ]; then
        echo -e " [${GREEN}OK${RESET}] Java version is ${BOLD}$JAVA_MAJOR${RESET} (meets >= 21 requirement)."
    else
        echo -e " [${RED}FAIL${RESET}] Detected Java version $JAVA_MAJOR. This curriculum requires Java 21 LTS or newer."
        ERRORS=$((ERRORS + 1))
    fi
fi

if command -v javac >/dev/null 2>&1; then
    JAVAC_RAW_VERSION=$(javac -version 2>&1)
    echo -e " Compiler: $JAVAC_RAW_VERSION"
fi

if command -v mvn >/dev/null 2>&1; then
    MVN_VERSION=$(mvn -version 2>&1 | head -n 1)
    echo -e " Build Tool: $MVN_VERSION"
fi

echo ""
echo -e "${BOLD}Verifying Bytecode Compilation with --release 21:${RESET}"
TMP_DIR=$(mktemp -d)
cat << 'EOF' > "$TMP_DIR/Probe.java"
public class Probe {
    public static void main(String[] args) {
        System.out.println("Java Environment OK");
    }
}
EOF

if javac --release 21 -d "$TMP_DIR" "$TMP_DIR/Probe.java" >/dev/null 2>&1; then
    RUN_OUT=$(java -cp "$TMP_DIR" Probe)
    if [ "$RUN_OUT" == "Java Environment OK" ]; then
        echo -e " [${GREEN}OK${RESET}] javac --release 21 test compile and execution passed."
    else
        echo -e " [${RED}FAIL${RESET}] Compiled probe executed with unexpected output: $RUN_OUT"
        ERRORS=$((ERRORS + 1))
    fi
else
    echo -e " [${RED}FAIL${RESET}] javac failed to compile targeting --release 21."
    ERRORS=$((ERRORS + 1))
fi
rm -rf "$TMP_DIR"

echo ""
if [ "$ERRORS" -eq 0 ]; then
    echo -e "${BOLD}${GREEN}All environment checks passed successfully!${RESET}"
    echo -e "You are ready to begin Phase 00 and Lesson 01."
    exit 0
else
    echo -e "${BOLD}${RED}Environment check encountered $ERRORS errors.${RESET}"
    echo -e "Please install or update your OpenJDK installation to JDK 21 LTS or newer."
    exit 1
fi
