#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CODE_DIR="${SCRIPT_DIR}/../code"

chmod +x "${CODE_DIR}/run_progressive_steps.sh"
"${CODE_DIR}/run_progressive_steps.sh"
