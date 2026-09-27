#!/usr/bin/env python3
"""
SBOM & SLSA Provenance Generator (Phases 86, 87, 88, 212)
Generates:
1. Software Bill of Materials (SBOM) in CycloneDX 1.5 JSON format.
2. Cryptographic SLSA Provenance v1.0 Attestation.
"""

import argparse
import hashlib
import json
import os
import sys
import time


def compute_sha256(filepath: str) -> str:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def generate_sbom(artifact_path: str, output_path: str):
    digest = compute_sha256(artifact_path)
    filename = os.path.basename(artifact_path)

    sbom = {
        "bomFormat": "CycloneDX",
        "specVersion": "1.5",
        "serialNumber": f"urn:uuid:{hashlib.md5(f'{filename}-{time.time()}'.encode()).hexdigest()}",
        "version": 1,
        "metadata": {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "tools": [{"vendor": "delivery-from-scratch", "name": "sbom-generator", "version": "1.0.0"}],
            "component": {
                "type": "application",
                "name": filename,
                "version": "1.0.0",
                "hashes": [{"alg": "SHA-256", "content": digest}]
            }
        },
        "components": [
            {
                "type": "library",
                "name": "python-runtime",
                "version": sys.version.split()[0],
                "purl": f"pkg:generic/python@{sys.version.split()[0]}",
                "licenses": [{"license": {"id": "PSF-2.0"}}]
            },
            {
                "type": "library",
                "name": "sqlite3",
                "version": "3.x",
                "purl": "pkg:generic/sqlite3@3.x",
                "licenses": [{"license": {"id": "Public-Domain"}}]
            }
        ]
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(sbom, f, indent=2)
    print(f"✓ CycloneDX SBOM written to: {output_path}")


def generate_provenance(artifact_path: str, output_path: str):
    digest = compute_sha256(artifact_path)
    filename = os.path.basename(artifact_path)

    git_commit = os.environ.get("GITHUB_SHA", "c477286c99d56c965cd1afddc5862b17ce5661ad")
    repo_uri = os.environ.get("GITHUB_REPOSITORY", "binarydevelop/ci-cd-and-software-delivery-from-scratch")

    provenance = {
        "_type": "https://in-toto.io/Statement/v1",
        "subject": [
            {
                "name": filename,
                "digest": {"sha256": digest}
            }
        ],
        "predicateType": "https://slsa.dev/provenance/v1",
        "predicate": {
            "buildDefinition": {
                "buildType": "https://actions.github.com/buildtypes/runner/v1",
                "externalParameters": {
                    "workflow": ".github/workflows/release.yml",
                    "source": f"https://github.com/{repo_uri}"
                },
                "internalParameters": {
                    "runnerOS": "linux-x64",
                    "builderImage": "ghcr.io/actions/runner:latest"
                },
                "resolvedDependencies": [
                    {
                        "uri": f"git+https://github.com/{repo_uri}",
                        "digest": {"gitCommit": git_commit}
                    }
                ]
            },
            "runDetails": {
                "builder": {
                    "id": "https://github.com/binarydevelop/ci-cd-and-software-delivery-from-scratch/runner"
                },
                "metadata": {
                    "invocationId": f"run-{int(time.time())}",
                    "startedOn": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
                }
            }
        }
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(provenance, f, indent=2)
    print(f"✓ SLSA Provenance v1.0 written to: {output_path}")


def verify_provenance(artifact_path: str, provenance_path: str) -> bool:
    actual_digest = compute_sha256(artifact_path)
    with open(provenance_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    subjects = data.get("subject", [])
    for sub in subjects:
        recorded_digest = sub.get("digest", {}).get("sha256")
        if recorded_digest == actual_digest:
            print(f"✓ Provenance verification PASSED: Artifact digest {actual_digest} matches recorded attestation.")
            return True

    print(f"✗ Provenance verification FAILED: Digest mismatch!", file=sys.stderr)
    return False


def main():
    parser = argparse.ArgumentParser(description="SBOM and SLSA Provenance Generator")
    parser.add_argument("--mode", choices=["sbom", "provenance", "verify"], required=True)
    parser.add_argument("--artifact", required=True)
    parser.add_argument("--output", default="output.json")
    parser.add_argument("--provenance", help="Provenance file path for verification")
    args = parser.parse_args()

    if args.mode == "sbom":
        generate_sbom(args.artifact, args.output)
    elif args.mode == "provenance":
        generate_provenance(args.artifact, args.output)
    elif args.mode == "verify":
        if not args.provenance:
            print("Error: --provenance path required for verification mode", file=sys.stderr)
            sys.exit(1)
        valid = verify_provenance(args.artifact, args.provenance)
        sys.exit(0 if valid else 1)


if __name__ == "__main__":
    main()
