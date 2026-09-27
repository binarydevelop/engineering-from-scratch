#!/usr/bin/env bash
# ==============================================================================
# Script: build.sh
# Purpose: Build software artifact from checked-out source commit.
# Stage: Phase 03, 43, 48, 50, 51
# Principle: Build Once — Same artifact promoted across all environments.
# ==============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
APP_DIR="${ROOT_DIR}/sample-apps/delivery-service"
BUILD_DIR="${ROOT_DIR}/outputs/build"

echo "========================================================================"
echo " Building Delivery Service Artifact"
echo "========================================================================"

# 1. Capture exact source identity (Phase 02, 03)
if git -C "${ROOT_DIR}" rev-parse HEAD >/dev/null 2>&1; then
    COMMIT_SHA=$(git -C "${ROOT_DIR}" rev-parse HEAD)
else
    COMMIT_SHA="unknown-dev-commit"
fi

BUILD_TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
VERSION=$(cat "${APP_DIR}/VERSION" 2>/dev/null || echo "1.0.0")

echo "Source Git Commit : ${COMMIT_SHA}"
echo "Build Timestamp   : ${BUILD_TIMESTAMP}"
echo "Release Version   : ${VERSION}"

# 2. Prepare clean build output directory
rm -rf "${BUILD_DIR}"
mkdir -p "${BUILD_DIR}/app"

# 3. Static Bytecode Compilation / Syntax Verification (Phase 43)
echo "Compiling Python source to bytecode..."
python3 -m py_compile "${APP_DIR}/app.py" "${APP_DIR}/db/migration_engine.py"

# 4. Copy distributable assets
cp "${APP_DIR}/app.py" "${BUILD_DIR}/app/"
cp -r "${APP_DIR}/db" "${BUILD_DIR}/app/"
cp "${APP_DIR}/Dockerfile" "${BUILD_DIR}/"

# 5. Generate Immutable Build Manifest (Phase 51)
cat <<EOF > "${BUILD_DIR}/build-manifest.json"
{
  "service": "delivery-service",
  "version": "${VERSION}",
  "git_commit": "${COMMIT_SHA}",
  "build_timestamp": "${BUILD_TIMESTAMP}",
  "builder": "scripts/build.sh",
  "python_version": "$(python3 --version | cut -d' ' -f2)",
  "build_host": "$(hostname)"
}
EOF

echo "✓ Build completed successfully. Output ready in outputs/build/"
