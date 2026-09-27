"""
Tests for Capstone 04: Production Readiness Review (PRR).
"""

import os
import sys
import pytest

APP_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "app")
if APP_DIR not in sys.path:
    sys.path.insert(0, APP_DIR)

from checklist import ProductionReadinessAuditor
from probes import ProbeManager
from reporter import ReportGenerator

def test_production_ready_service_passes():
    auditor = ProductionReadinessAuditor()
    valid_config = {
        "SECRET_KEY": "a" * 32,
        "ENABLE_HEALTH_PROBE": True,
        "CORS_ORIGINS": ["https://app.example.com"],
        "ENABLE_METRICS": True,
        "JSON_LOGS": True,
        "REQUEST_TIMEOUT_SEC": 5.0
    }

    result = auditor.audit(valid_config)
    assert result.passed is True
    assert result.score == 5
    assert result.percentage == 100.0

    report = ReportGenerator.to_markdown(result)
    assert "APPROVED FOR PRODUCTION" in report

def test_unready_service_fails_audit():
    auditor = ProductionReadinessAuditor()
    bad_config = {
        "SECRET_KEY": "changeme",
        "ENABLE_HEALTH_PROBE": False,
        "CORS_ORIGINS": ["*"],
        "ENABLE_METRICS": False,
        "JSON_LOGS": False,
        "REQUEST_TIMEOUT_SEC": 120.0
    }

    result = auditor.audit(bad_config)
    assert result.passed is False
    assert result.score == 0

    report = ReportGenerator.to_markdown(result)
    assert "REJECTED - REMEDIATION REQUIRED" in report

def test_probe_manager_evaluates_readiness():
    probes = ProbeManager()
    probes.register_dependency("primary_db", lambda: True)
    probes.register_dependency("redis_cache", lambda: False)  # Failed dependency

    assert probes.check_liveness()["status"] == "ALIVE"
    
    ready_status = probes.check_readiness()
    assert ready_status["status"] == "NOT_READY"
    assert "redis_cache" in ready_status["unhealthy"]
