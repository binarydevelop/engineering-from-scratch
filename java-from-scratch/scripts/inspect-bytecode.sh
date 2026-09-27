#!/usr/bin/env bash
# ==============================================================================
# Helper to compile a Java file and disassemble it with javap
# Usage: ./scripts/inspect-bytecode.sh path/to/Source.java [verbose]
# ==============================================================================

set -euo pipefail

if [ $# -lt 1 ]; then
    echo "Usage: $0 <path-to-java-file> [verbose]"
    echo "Example: $0 phases/phase-01-source-to-bytecode/src/Hello.java"
    exit 1
fi

JAVA_FILE="$1"
VERBOSE="${2:-false}"

if [ ! -f "$JAVA_FILE" ]; then
    echo "Error: File $JAVA_FILE not found."
    exit 1
fi

TMP_DIR=$(mktemp -d)
trap 'rm -rf "$TMP_DIR"' EXIT

echo "Compiling $JAVA_FILE with --release 21..."
javac --release 21 -g -d "$TMP_DIR" "$JAVA_FILE"

# Find generated class files
CLASS_FILES=$(find "$TMP_DIR" -name "*.class")

for CLASS_FILE in $CLASS_FILES; do
    CLASS_NAME=$(basename "$CLASS_FILE")
    echo "======================================================================"
    echo "Bytecode Disassembly for: $CLASS_NAME"
    echo "======================================================================"
    if [ "$VERBOSE" = "true" ] || [ "$VERBOSE" = "-v" ]; then
        javap -c -v -p "$CLASS_FILE"
    else
        javap -c -p "$CLASS_FILE"
    fi
    echo ""
done
