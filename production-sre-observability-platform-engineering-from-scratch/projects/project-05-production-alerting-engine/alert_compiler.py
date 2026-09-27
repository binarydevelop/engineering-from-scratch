"""
Project 05: Production Alerting Engine & Route Compiler.
"""
from typing import Dict, Any, List

def compile_alert_rule(name: str, metric: str, threshold: float, duration: str, severity: str) -> Dict[str, Any]:
    return {
        "alert": name,
        "expr": f"{metric} > {threshold}",
        "for": duration,
        "labels": {
            "severity": severity,
            "tier": "tier-1"
        },
        "annotations": {
            "summary": f"Alert {name} triggered on {metric}"
        }
    }
