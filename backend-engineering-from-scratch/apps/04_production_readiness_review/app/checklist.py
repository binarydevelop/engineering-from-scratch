"""
Production Readiness Review (PRR) audit engine.
Evaluates service configuration across 5 operational dimensions.
"""

from typing import Dict, Any, List

class AuditResult:
    def __init__(self, passed: bool, score: int, max_score: int, findings: List[Dict[str, str]]):
        self.passed = passed
        self.score = score
        self.max_score = max_score
        self.percentage = round((score / max_score) * 100, 1) if max_score > 0 else 0.0
        self.findings = findings

class ProductionReadinessAuditor:
    def __init__(self):
        pass

    def audit(self, config: Dict[str, Any]) -> AuditResult:
        findings = []
        score = 0
        max_score = 5

        # Check 1: Secrets & Env Variables
        secret_key = config.get("SECRET_KEY", "")
        if not secret_key or secret_key in ("secret", "changeme", "default", "123456"):
            findings.append({"check": "Secrets", "status": "FAIL", "msg": "Insecure or default SECRET_KEY detected"})
        elif len(secret_key) < 32:
            findings.append({"check": "Secrets", "status": "WARN", "msg": "SECRET_KEY entropy is less than 32 characters"})
            score += 1
        else:
            findings.append({"check": "Secrets", "status": "PASS", "msg": "Cryptographically secure secret key configured"})
            score += 1

        # Check 2: Health Probes
        has_healthz = config.get("ENABLE_HEALTH_PROBE", False)
        if not has_healthz:
            findings.append({"check": "Health Probes", "status": "FAIL", "msg": "No health/liveness probe enabled"})
        else:
            findings.append({"check": "Health Probes", "status": "PASS", "msg": "Health probe endpoint enabled"})
            score += 1

        # Check 3: CORS Security
        cors_origins = config.get("CORS_ORIGINS", [])
        if "*" in cors_origins:
            findings.append({"check": "CORS Security", "status": "FAIL", "msg": "Wildcard '*' CORS origin is hazardous in production"})
        elif not cors_origins:
            findings.append({"check": "CORS Security", "status": "WARN", "msg": "No CORS origins defined"})
        else:
            findings.append({"check": "CORS Security", "status": "PASS", "msg": "Restricted CORS origins configured"})
            score += 1

        # Check 4: Observability (Metrics & Logs)
        metrics_enabled = config.get("ENABLE_METRICS", False)
        structured_logs = config.get("JSON_LOGS", False)
        if not metrics_enabled or not structured_logs:
            findings.append({"check": "Observability", "status": "FAIL", "msg": "Structured JSON logging and metrics required"})
        else:
            findings.append({"check": "Observability", "status": "PASS", "msg": "Observability pipeline verified"})
            score += 1

        # Check 5: Timeout Boundaries
        timeout = config.get("REQUEST_TIMEOUT_SEC", 0)
        if timeout <= 0 or timeout > 30:
            findings.append({"check": "Timeouts", "status": "FAIL", "msg": f"Invalid request timeout ({timeout}s); should be between 1-30s"})
        else:
            findings.append({"check": "Timeouts", "status": "PASS", "msg": f"Appropriate timeout boundary set ({timeout}s)"})
            score += 1

        is_passed = (score >= 4) and not any(f["status"] == "FAIL" and f["check"] in ("Secrets", "Health Probes") for f in findings)
        return AuditResult(is_passed, score, max_score, findings)
