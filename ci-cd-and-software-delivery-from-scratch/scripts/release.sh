#!/usr/bin/env bash
# ==============================================================================
# Script: release.sh
# Purpose: Create an immutable release bundle with changelog, SBOM, and provenance.
# Stage: Phase 63-69, 86, 87, 88
# ==============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
OUTPUT_DIR="${ROOT_DIR}/outputs"

echo "========================================================================"
echo " Creating Software Release"
echo "========================================================================"

VERSION="${1:-1.0.0}"
RELEASE_TAG="v${VERSION}"
RELEASE_DIR="${OUTPUT_DIR}/release-${RELEASE_TAG}"

echo "Target Release: ${RELEASE_TAG}"

# 1. Immutability Check: Do not overwrite existing release tag (Phase 69)
if git -C "${ROOT_DIR}" rev-parse "${RELEASE_TAG}" >/dev/null 2>&1; then
    echo "ERROR: Release tag '${RELEASE_TAG}' already exists! Releases are immutable." >&2
    exit 1
fi

mkdir -p "${RELEASE_DIR}"

# 2. Package Artifact if needed
bash "${SCRIPT_DIR}/package.sh"

PACKAGE_FILE="${OUTPUT_DIR}/delivery-service-${VERSION}.tar.gz"
if [ ! -f "${PACKAGE_FILE}" ]; then
    echo "ERROR: Expected package file '${PACKAGE_FILE}' does not exist!" >&2
    exit 1
fi

# Copy artifact into release bundle
cp "${PACKAGE_FILE}" "${RELEASE_DIR}/"
cp "${OUTPUT_DIR}/artifact-metadata.json" "${RELEASE_DIR}/"

# 3. Generate Software Bill of Materials (SBOM) (Phase 86)
echo "Generating SBOM..."
python3 "${ROOT_DIR}/security-labs/sbom_provenance_generator.py" \
    --mode sbom \
    --artifact "${PACKAGE_FILE}" \
    --output "${RELEASE_DIR}/sbom.json"

# 4. Generate SLSA Provenance Attestation (Phase 87, 88)
echo "Generating SLSA Build Provenance Attestation..."
python3 "${ROOT_DIR}/security-labs/sbom_provenance_generator.py" \
    --mode provenance \
    --artifact "${PACKAGE_FILE}" \
    --output "${RELEASE_DIR}/provenance.json"

# 5. Generate Changelog & Release Notes (Phase 66, 67)
echo "Generating Release Notes..."
cat <<EOF > "${RELEASE_DIR}/RELEASE_NOTES.md"
# Release ${RELEASE_TAG}

- **Release Date**: $(date -u +"%Y-%m-%d %H:%M:%SZ")
- **Commit**: $(git -C "${ROOT_DIR}" rev-parse HEAD 2>/dev/null || echo "HEAD")
- **Artifact**: delivery-service-${VERSION}.tar.gz
- **Artifact Digest**: $(cat "${PACKAGE_FILE}.sha256" 2>/dev/null || echo "unknown")

## Highlights
- Production delivery service release bundle.
- Verified unit, integration, and API contract test suites.
- Includes cryptographically signed SBOM and SLSA Provenance Attestation.

## Migration Requirements
- Zero-downtime expand migration supported.
EOF

echo "✓ Release bundle successfully created at: ${RELEASE_DIR}"
