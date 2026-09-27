"""
Tests for Project: High-Throughput Analytics Ingestion API
"""

import pytest
import os
import sys
import importlib.util

PROJ_DIR = os.path.dirname(os.path.abspath(__file__))
APP_FILE = os.path.join(os.path.dirname(PROJ_DIR), "app", "main.py")

spec = importlib.util.spec_from_file_location("proj_08_analytics_event_api", APP_FILE)
proj = importlib.util.module_from_spec(spec)
spec.loader.exec_module(proj)

globals().update({k: getattr(proj, k) for k in dir(proj) if not k.startswith("__")})

def test_analytics_buffering_and_flush():
    ingestor = AnalyticsIngestor(buffer_capacity=5)
    for i in range(5):
        assert ingestor.ingest({"event": f"click_{i}"}) is True

    # Buffer is full -> backpressure rejects
    assert ingestor.ingest({"event": "overflow"}) is False

    flushed = ingestor.flush()
    assert flushed == 5
    assert len(ingestor.buffer) == 0
