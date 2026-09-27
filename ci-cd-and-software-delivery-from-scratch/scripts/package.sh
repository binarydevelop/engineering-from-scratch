#!/usr/bin/env bash
# ==============================================================================
# Script: package.sh
# Purpose: Package build output into an immutable, hashed release artifact.
# Stage: Phase 49, 51, 57, 85
# ==============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
BUILD_DIR="${ROOT_DIR}/outputs/build"
OUTPUT_DIR="${ROOT_DIR}/outputs"

echo "========================================================================"
echo " Packaging Software Artifact"
echo "========================================================================"

if [ ! -d "${BUILD_DIR}" ]; then
    echo "Build directory not found. Running build.sh first..."
    bash "${SCRIPT_DIR}/build.sh"
fi

VERSION=$(grep -o '"version": "[^"]*"' "${BUILD_DIR}/build-manifest.json" | cut -d'"' -f4 || echo "1.0.0")
COMMIT_SHA=$(grep -o '"git_commit": "[^"]*"' "${BUILD_DIR}/build-manifest.json" | cut -d'"' -f4 || echo "unknown")
PACKAGE_NAME="delivery-service-${VERSION}.tar.gz"
TARGET_ARCHIVE="${OUTPUT_DIR}/${PACKAGE_NAME}"

# 1. Create compressed tarball artifact
echo "Creating archive: ${TARGET_ARCHIVE}..."
tar -czf "${TARGET_ARCHIVE}" -C "${BUILD_DIR}" app build-manifest.json

# 2. Compute cryptographic SHA-256 digest (Phase 51, 85)
if command -v sha256sum >/dev/null 2>&1; then
    DIGEST=$(sha256sum "${TARGET_ARCHIVE}" | awk '{print $1}')
else
    DIGEST=$(shasum -a 256 "${TARGET_ARCHIVE}" | awk '{print $1}')
fi

echo "sha256:${DIGEST}" > "${OUTPUT_DIR}/${PACKAGE_NAME}.sha256"

# 3. Create full artifact metadata record
cat <<EOF > "${OUTPUT_DIR}/artifact-metadata.json"
{
  "artifact_name": "${PACKAGE_NAME}",
  "artifact_type": "tarball",
  "version": "${VERSION}",
  "git_commit": "${COMMIT_SHA}",
  "sha256_digest": "${DIGEST}",
  "size_bytes": $(wc -c < "${TARGET_ARCHIVE}" | tr -d ' '),
  "packaged_at": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
}
EOF

echo "✓ Artifact packaged successfully:"
echo "    File   : ${TARGET_ARCHIVE}"
echo "    Digest : sha256:${DIGEST}"
echo "    Metadata: ${OUTPUT_DIR}/artifact-metadata.json"
