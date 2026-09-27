#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CODE_DIR="${SCRIPT_DIR}/../code"

chmod +x "${CODE_DIR}/trace_full_stack.py"
python3 "${CODE_DIR}/trace_full_stack.py"
