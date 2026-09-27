#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "Resetting all NoSQL datasets to pristine seed state..."
python3 "${BASE_DIR}/scripts/seed-data.py"

echo "Pruned and re-generated JSON datasets in ${BASE_DIR}/datasets/"
