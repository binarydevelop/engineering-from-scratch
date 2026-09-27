"""
Production Readiness Scorecard Evaluator.

Audits a service repository or configuration against production readiness invariants:
ownership, telemetry, health probes, resource limits, and SLO definitions.
"""

import os
import re
from typing import Dict, Any, List


def evaluate_service_directory(service_dir: str) -> Dict[str, Any]:
    checks = {
        "health_probes": False,
        "metrics_endpoint": False,
        "structured_logging": False,
        "graceful_shutdown": False,
        "resource_limits": False,
        "ownership_documented": False,
    }
    details: List[str] = []

    if not os.path.isdir(service_dir):
        return {"error": f"Directory not found: {service_dir}"}

    # Inspect all python and yaml files in directory
    combined_content = ""
    for root, _, files in os.walk(service_dir):
        for f in files:
            if f.endswith((".py", ".yaml", ".yml", "Dockerfile", ".json")):
                filepath = os.path.join(root, f)
                try:
                    with open(filepath, "r", encoding="utf-8") as fh:
                        combined_content += fh.read() + "\n"
                except Exception:
                    pass

    # Check 1: Health probes
    if "/healthz" in combined_content and "/ready" in combined_content:
        checks["health_probes"] = True
        details.append("[PASS] Health endpoints (/healthz, /ready) present.")
    else:
        details.append("[FAIL] Missing standard /healthz and /ready endpoints.")

    # Check 2: Metrics endpoint
    if "/metrics" in combined_content or "generate_latest" in combined_content:
        checks["metrics_endpoint"] = True
        details.append("[PASS] Prometheus /metrics endpoint configured.")
    else:
        details.append("[FAIL] Missing Prometheus /metrics endpoint.")

    # Check 3: Structured logging / correlation ID
    if "correlation_id" in combined_content or "structured_logging" in combined_content:
        checks["structured_logging"] = True
        details.append("[PASS] Correlation ID & structured logging detected.")
    else:
        details.append("[FAIL] Missing correlation ID or structured logging.")

    # Check 4: Graceful shutdown
    if "SIGTERM" in combined_content or "timeout-graceful-shutdown" in combined_content or "timeout_keep_alive" in combined_content:
        checks["graceful_shutdown"] = True
        details.append("[PASS] Graceful shutdown handling configured.")
    else:
        details.append("[FAIL] No explicit SIGTERM graceful shutdown handling found.")

    # Check 5: Resource limits
    if "cpu_limit" in combined_content or "resources:" in combined_content or "memory_limit" in combined_content:
        checks["resource_limits"] = True
        details.append("[PASS] Explicit resource limits declared.")
    else:
        details.append("[FAIL] No CPU or Memory resource limits declared.")

    # Check 6: Ownership
    if "team:" in combined_content or "owner" in combined_content:
        checks["ownership_documented"] = True
        details.append("[PASS] Owning team explicitly documented.")
    else:
        details.append("[FAIL] Owning team metadata missing.")

    passed_count = sum(1 for v in checks.values() if v)
    total_checks = len(checks)
    score_percent = (passed_count / total_checks) * 100.0

    if score_percent >= 90:
        grade = "A (Production Certified)"
    elif score_percent >= 70:
        grade = "B (Acceptable with Warnings)"
    elif score_percent >= 50:
        grade = "C (Significant Gaps)"
    else:
        grade = "F (Not Ready for Production Traffic)"

    return {
        "service_dir": service_dir,
        "score_percent": score_percent,
        "grade": grade,
        "passed_count": passed_count,
        "total_checks": total_checks,
        "checks": checks,
        "details": details
    }
