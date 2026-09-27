"""
Project 08: Production Readiness Review (PRR) Linter.
"""
from typing import Dict, Any, List

def lint_production_readiness(service_spec: Dict[str, Any]) -> Dict[str, Any]:
    checks = {
        "has_health_check": bool(service_spec.get("health_check_endpoint")),
        "has_metrics": bool(service_spec.get("metrics_endpoint")),
        "has_resource_limits": bool(service_spec.get("resources", {}).get("limits")),
        "has_slo_defined": bool(service_spec.get("slo")),
        "has_runbook": bool(service_spec.get("runbook_url"))
    }
    score = (sum(1 for v in checks.values() if v) / len(checks)) * 100
    return {
        "score_percent": score,
        "is_ready": score >= 80.0,
        "checks": checks
    }
