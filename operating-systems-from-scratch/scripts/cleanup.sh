#!/usr/bin/env bash
# cleanup.sh: Clean build artifacts, temporary test files, and stale lab processes
set -euo pipefail

echo "Cleaning operating-systems-from-scratch artifacts..."

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# 1. Clean binaries and object files
find "${REPO_ROOT}" -type f \( -name "*.o" -o -name "*.out" -o -name "*.dylib" -o -name "*.so" \) -delete 2>/dev/null || true
find "${REPO_ROOT}" -type f \( -name "scratch_disk.img" -o -name "test.txt" -o -name "out.txt" -o -name "input.txt" \) -delete 2>/dev/null || true
find "${REPO_ROOT}" -type f -name "*.pyc" -delete 2>/dev/null || true
find "${REPO_ROOT}" -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true

# 2. Clean compiled binaries in projects and benchmarks
rm -rf "${REPO_ROOT}/bin" "${REPO_ROOT}/build"
mkdir -p "${REPO_ROOT}/bin"

# 3. Clean any dangling test server sockets
find "${REPO_ROOT}" -type s -delete 2>/dev/null || true

echo "Cleanup complete."
