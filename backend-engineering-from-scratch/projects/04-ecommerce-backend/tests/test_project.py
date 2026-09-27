"""
Tests for Project: E-Commerce Transaction Backend
"""

import pytest
import os
import sys
import importlib.util

PROJ_DIR = os.path.dirname(os.path.abspath(__file__))
APP_FILE = os.path.join(os.path.dirname(PROJ_DIR), "app", "main.py")

spec = importlib.util.spec_from_file_location("proj_04_ecommerce_backend", APP_FILE)
proj = importlib.util.module_from_spec(spec)
spec.loader.exec_module(proj)

globals().update({k: getattr(proj, k) for k in dir(proj) if not k.startswith("__")})

def test_atomic_order_and_outbox():
    svc = ECommerceService()
    order = svc.place_order("ord_101", "prod_1", 1)
    assert order["status"] == "CONFIRMED"
    assert svc.inventory["prod_1"] == 0
    assert len(svc.outbox) == 1
    assert svc.outbox[0]["event"] == "OrderPlaced"

    import pytest
    with pytest.raises(ValueError):
        svc.place_order("ord_102", "prod_1", 1)
