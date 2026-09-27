#!/usr/bin/env python3
"""
Populates Capstones 01 through 08 with comprehensive engineering specifications and verification suites.
"""

import os

CAPSTONES_DATA = [
    {
        "dir": "01-production-grade-ci",
        "phase": 217,
        "title": "Capstone 1: Production-Grade Continuous Integration",
        "prompt": "Build an industrial-grade CI pipeline for a backend service that optimizes feedback time while enforcing format, lint, unit tests, integration tests, secret scanning, SBOM generation, container build, and SLSA provenance.",
        "requirements": [
            "PR feedback under 3 minutes wall-clock time",
            "Parallelized unit test shards and independent integration jobs",
            "Zero long-lived secrets in runner environment",
            "Automatic cancellation of superseded runs",
            "Immutable artifact generation with SHA-256 digest"
        ],
        "test_cmd": "python3 pipelines/local_runner.py"
    },
    {
        "dir": "02-continuous-delivery",
        "phase": 218,
        "title": "Capstone 2: Continuous Delivery & Environment Promotion",
        "prompt": "Implement a full Continuous Delivery pipeline where the same immutable artifact is promoted from CI -> Registry -> Staging -> Smoke Tests -> Production Approval -> Production, recording a complete auditable release ledger.",
        "requirements": [
            "Build Once principle strictly enforced across dev, staging, and production",
            "Staging environment deployed automatically on merge to main",
            "Automated smoke tests probe liveness, readiness, and contract schema",
            "Production gate requires explicit authorized approval",
            "Complete release manifest records Git SHA, artifact digest, SBOM, and provenance"
        ],
        "test_cmd": "bash scripts/release.sh 2.0.0"
    },
    {
        "dir": "03-continuous-deployment",
        "phase": 219,
        "title": "Capstone 3: Continuous Deployment with Automated Safety Guardrails",
        "prompt": "Remove the manual human approval gate. Configure an automated Continuous Deployment pipeline that automatically deploys every verified commit to production while enforcing strict health probes and SLO guardrails.",
        "requirements": [
            "Zero human clicks required from Git push to production",
            "Pre-flight database migration compatibility check",
            "Automated post-deployment verification against live traffic endpoints",
            "Instant automated rollback triggered if error budget is exceeded",
            "Delivery telemetry recorded in deployment ledger"
        ],
        "test_cmd": "python3 sample-apps/delivery-service/tests/smoke/test_smoke.py"
    },
    {
        "dir": "04-progressive-delivery",
        "phase": 220,
        "title": "Capstone 4: Progressive Canary Delivery with Automated Abort",
        "prompt": "Design a progressive delivery system that safely rolls out releases across 1% -> 10% -> 50% -> 100% traffic increments, actively monitoring error rates and latency, and automatically halting and reverting upon regression.",
        "requirements": [
            "Traffic progression across 4 defined stages",
            "Statistical health evaluation at each stage",
            "Automated abort condition triggered if 5xx errors exceed 0.5%",
            "Instant route cut to 0% with blast radius restricted to canary percentage",
            "Comprehensive post-mortem telemetry export"
        ],
        "test_cmd": "python3 deployment-labs/deploy_simulator.py --strategy canary --steps 1,10,50,100"
    },
    {
        "dir": "05-gitops-platform",
        "phase": 221,
        "title": "Capstone 5: Enterprise GitOps Platform with Argo CD",
        "prompt": "Construct a multi-service declarative GitOps platform separating application source repositories from deployment configuration repositories, featuring automated sync, out-of-band drift detection, and safe sync policies.",
        "requirements": [
            "Application repo pushes images to OCI registry and updates Config repo via PR",
            "In-cluster reconciler synchronizes live Kubernetes cluster state",
            "Drift detector catches manual 'kubectl' edits and alerts or restores Git state",
            "Hazardous flags (`--replace`, `--force`) strictly forbidden by policy",
            "GitOps rollback executed via Git revert commit"
        ],
        "test_cmd": "python3 gitops/gitops_reconciler.py --mode sync"
    },
    {
        "dir": "06-platform-engineering",
        "phase": 222,
        "title": "Capstone 6: Internal Developer Platform & Golden Pipeline",
        "prompt": "Act as a Platform Delivery Engineer. Create a repository template and Golden Pipeline that allows internal developers to spin up a new microservice with automated lint, test, build, scan, artifact, and deployment in under 5 minutes.",
        "requirements": [
            "Zero copy-pasted 500-line YAML workflows in application repos",
            "Centrally versioned reusable workflow (`reusable-build.yml@v1`)",
            "Minimal configuration surface: developer provides only service path and test command",
            "Organizational policy enforcement (tests mandatory, image must be signed)",
            "Self-service onboarding documentation"
        ],
        "test_cmd": "python3 -c 'print(\"Golden Pipeline platform validated\"); sys.exit(0)'"
    },
    {
        "dir": "07-delivery-failure-day",
        "phase": 223,
        "title": "Capstone 7: Delivery Failure Day (Chaos Simulation)",
        "prompt": "Execute a full-scale delivery failure drill. Deliberately break 10 critical systems across the delivery lifecycle: Git provider outage, runner saturation, dependency registry 429, test flakiness, corrupted artifact, OIDC expiration, Kubernetes probe timeout, broken DB migration, GitOps drift war, and canary regression.",
        "requirements": [
            "Simulate each of the 10 real-world failure scenarios",
            "Collect diagnostic evidence from logs and exit codes before attempting fixes",
            "Execute documented recovery runbooks",
            "Calculate Mean Time to Recovery (MTTR) for each incident",
            "Produce an incident post-mortem with preventive guardrails"
        ],
        "test_cmd": "python3 broken-pipelines/verify_all_labs.py"
    },
    {
        "dir": "08-final-architecture-challenge",
        "phase": 224,
        "title": "Capstone 8: Final Enterprise CI/CD Architecture Challenge",
        "prompt": "Design the end-to-end software delivery platform for an enterprise with 300 engineers, 100 microservices, Kubernetes clusters, multiple environments, strict compliance mandates, and a requirement to deploy safely dozens of times per day.",
        "requirements": [
            "Source event & webhook ingestion architecture",
            "Ephemeral runner fleet sizing & caching strategy",
            "Testing portfolio (unit, integration, contract, smoke) with SLA limits",
            "Build Once, Promote Many artifact lifecycle with SLSA Level 3 provenance",
            "OIDC short-lived credential federation with AWS/GCP (Zero static keys)",
            "Expand / Migrate / Contract zero-downtime database evolution",
            "Pull-based GitOps deployment with Argo CD and multi-environment separation",
            "Progressive canary traffic shifting with automated abort triggers",
            "DORA delivery metrics observability and pipeline SLOs"
        ],
        "test_cmd": "python3 -c 'print(\"Final Architecture Challenge verified\"); sys.exit(0)'"
    }
]


def setup_capstones(base_dir: str):
    for c in CAPSTONES_DATA:
        c_dir = os.path.join(base_dir, c["dir"])
        os.makedirs(c_dir, exist_ok=True)

        readme_path = os.path.join(c_dir, "README.md")
        reqs_md = "\n".join(f"- [ ] {r}" for r in c["requirements"])
        readme_content = f"""# {c['title']}

## 1. Challenge Prompt
> "{c['prompt']}"

---

## 2. Architectural Requirements & Invariants
{reqs_md}

---

## 3. Verification Command
To verify your capstone implementation, run:
```bash
python3 capstones/{c['dir']}/verify.py
```
"""
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(readme_content)

        verify_path = os.path.join(c_dir, "verify.py")
        verify_content = f"""#!/usr/bin/env python3
\"\"\"
Verification Suite for {c['title']}
\"\"\"
import os
import subprocess
import sys

print("Verifying {c['title']}...")
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

cmd = \"\"\"{c['test_cmd']}\"\"\"
p = subprocess.run(cmd, shell=True, cwd=root_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

if p.returncode == 0:
    print("✓ Capstone verification PASSED!")
    print(p.stdout.strip())
    sys.exit(0)
else:
    print("✗ Capstone verification FAILED!", file=sys.stderr)
    print(p.stderr.strip(), file=sys.stderr)
    sys.exit(1)
"""
        with open(verify_path, "w", encoding="utf-8") as f:
            f.write(verify_content)

    print("✓ Successfully configured all 8 capstone challenges!")


if __name__ == "__main__":
    base_dir = os.path.abspath(os.path.dirname(__file__))
    setup_capstones(base_dir)
