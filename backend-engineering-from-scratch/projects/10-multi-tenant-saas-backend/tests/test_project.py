"""
Tests for Project: Multi-Tenant SaaS Backend
"""

import pytest
import os
import sys
import importlib.util

PROJ_DIR = os.path.dirname(os.path.abspath(__file__))
APP_FILE = os.path.join(os.path.dirname(PROJ_DIR), "app", "main.py")

spec = importlib.util.spec_from_file_location("proj_10_multi_tenant_saas_backend", APP_FILE)
proj = importlib.util.module_from_spec(spec)
spec.loader.exec_module(proj)

globals().update({k: getattr(proj, k) for k in dir(proj) if not k.startswith("__")})

def test_multi_tenant_isolation():
    store = MultiTenantStore()
    store.insert("org_acme", "Acme Secret Strategy")
    store.insert("org_beta", "Beta Public Road")

    acme_docs = store.query("org_acme")
    assert len(acme_docs) == 1
    assert acme_docs[0]["title"] == "Acme Secret Strategy"

    beta_docs = store.query("org_beta")
    assert len(beta_docs) == 1
    assert beta_docs[0]["title"] == "Beta Public Road"
