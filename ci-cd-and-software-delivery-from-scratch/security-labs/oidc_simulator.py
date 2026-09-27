#!/usr/bin/env python3
"""
OIDC / Workload Identity Federation Simulator (Phases 77, 211)
Demonstrates:
- Ephemeral JWT generation by CI runner
- Cloud STS trust policy verification (repository, ref, workflow identity)
- Short-lived token issuance (15-minute TTL)
- Prevention of permanent credential exfiltration
"""

import base64
import hashlib
import hmac
import json
import sys
import time
from typing import Dict, Any, Optional

SIMULATED_PRIVATE_OIDC_SECRET = "github-actions-issuer-signing-key-educational"


def create_simulated_oidc_jwt(repo: str, ref: str, workflow: str, actor: str) -> str:
    """Generates a mock JWT matching GitHub Actions OIDC token claim schema."""
    header = {"alg": "HS256", "typ": "JWT"}
    now = int(time.time())
    payload = {
        "iss": "https://token.actions.githubusercontent.com",
        "sub": f"repo:{repo}:ref:{ref}",
        "aud": "sts.amazonaws.com",
        "ref": ref,
        "sha": "c477286c99d56c965cd1afddc5862b17ce5661ad",
        "repository": repo,
        "repository_owner": repo.split("/")[0] if "/" in repo else "unknown",
        "actor": actor,
        "workflow": workflow,
        "iat": now,
        "nbf": now,
        "exp": now + 900  # 15 minutes TTL
    }

    def b64url(data: bytes) -> str:
        return base64.urlsafe_b64encode(data).rstrip(b'=').decode('utf-8')

    hdr_b64 = b64url(json.dumps(header).encode())
    payload_b64 = b64url(json.dumps(payload).encode())
    signing_input = f"{hdr_b64}.{payload_b64}".encode()
    signature = hmac.new(SIMULATED_PRIVATE_OIDC_SECRET.encode(), signing_input, hashlib.sha256).digest()
    sig_b64 = b64url(signature)

    return f"{hdr_b64}.{payload_b64}.{sig_b64}"


class CloudSecurityTokenService:
    """Simulates AWS/GCP/Azure STS exchange with OIDC trust policy."""
    def __init__(self, allowed_repo: str, allowed_ref: str):
        self.allowed_repo = allowed_repo
        self.allowed_ref = allowed_ref

    def exchange_token(self, jwt_token: str) -> Dict[str, Any]:
        parts = jwt_token.split(".")
        if len(parts) != 3:
            raise ValueError("Malformed JWT structure")

        payload_bytes = base64.urlsafe_b64decode(parts[1] + "==")
        payload = json.loads(payload_bytes.decode())

        # Verify signature
        signing_input = f"{parts[0]}.{parts[1]}".encode()
        expected_sig = hmac.new(SIMULATED_PRIVATE_OIDC_SECRET.encode(), signing_input, hashlib.sha256).digest()
        provided_sig = base64.urlsafe_b64decode(parts[2] + "==")
        if not hmac.compare_digest(expected_sig, provided_sig):
            raise PermissionError("OIDC Token signature verification failed!")

        # Verify claims against IAM Trust Policy
        if payload.get("repository") != self.allowed_repo:
            raise PermissionError(f"Access Denied: Untrusted repository '{payload.get('repository')}'")
        if payload.get("ref") != self.allowed_ref:
            raise PermissionError(f"Access Denied: Untrusted ref '{payload.get('ref')}' — policy requires '{self.allowed_ref}'")

        # Success: Return short-lived credentials
        session_token = "sts_temp_" + hashlib.sha256(f"{time.time()}".encode()).hexdigest()[:32]
        return {
            "status": "AUTHORIZED",
            "AccessKeyId": "ASIA_TEMP_WORKLOAD_IDENTITY",
            "SecretAccessKey": session_token,
            "SessionToken": "iq_oidc_validated_session",
            "Expiration": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(payload["exp"])),
            "Scope": "production:deploy"
        }


def main():
    print("=== OIDC WORKLOAD IDENTITY FEDERATION SIMULATOR ===")
    repo = "binarydevelop/ci-cd-and-software-delivery-from-scratch"
    trusted_ref = "refs/heads/main"

    sts = CloudSecurityTokenService(allowed_repo=repo, allowed_ref=trusted_ref)

    # Scenario A: Legitimate CI workflow on main branch
    print("\n[Scenario 1] Legitimate Workflow on main branch:")
    valid_jwt = create_simulated_oidc_jwt(repo, "refs/heads/main", "deploy.yml", "release-bot")
    print(f"  Generated OIDC JWT token: {valid_jwt[:35]}...[truncated]")
    creds = sts.exchange_token(valid_jwt)
    print("  ✓ STS Token Exchange SUCCEEDED!")
    print(f"    Temporary Access Key: {creds['AccessKeyId']}")
    print(f"    Expiration: {creds['Expiration']} (TTL: 15 minutes)")

    # Scenario B: Untrusted Pull Request from a fork
    print("\n[Scenario 2] Untrusted Pull Request from external fork attempting STS exchange:")
    untrusted_jwt = create_simulated_oidc_jwt("attacker-fork/ci-cd-and-software-delivery-from-scratch", "refs/pull/42/merge", "deploy.yml", "external-user")
    try:
        sts.exchange_token(untrusted_jwt)
        print("  ✗ ERROR: Untrusted fork was authorized!", file=sys.stderr)
        sys.exit(1)
    except PermissionError as e:
        print(f"  ✓ SECURITY ENFORCED: STS rejected exchange: {e}")

    # Scenario C: Branch mismatch (feature branch trying to get production deploy role)
    print("\n[Scenario 3] Feature branch attempting to assume production deployment role:")
    feature_jwt = create_simulated_oidc_jwt(repo, "refs/heads/feature/test-change", "ci.yml", "dev-user")
    try:
        sts.exchange_token(feature_jwt)
        print("  ✗ ERROR: Feature branch was authorized!", file=sys.stderr)
        sys.exit(1)
    except PermissionError as e:
        print(f"  ✓ SECURITY ENFORCED: STS rejected exchange: {e}")

    print("\n✓ All OIDC identity federation scenarios validated successfully.")


if __name__ == "__main__":
    main()
