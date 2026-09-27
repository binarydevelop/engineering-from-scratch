"""
Tests for Project: Asynchronous File Processing Pipeline
"""

import pytest
import os
import sys
import importlib.util

PROJ_DIR = os.path.dirname(os.path.abspath(__file__))
APP_FILE = os.path.join(os.path.dirname(PROJ_DIR), "app", "main.py")

spec = importlib.util.spec_from_file_location("proj_07_file_processing_service", APP_FILE)
proj = importlib.util.module_from_spec(spec)
spec.loader.exec_module(proj)

globals().update({k: getattr(proj, k) for k in dir(proj) if not k.startswith("__")})

def test_file_pipeline_worker():
    pipeline = FilePipeline()
    fid = pipeline.upload_file("avatar.png", b"raw_image_bytes")
    assert pipeline.jobs[fid]["status"] == "PENDING"
    
    pipeline.process_file_worker(fid)
    assert pipeline.jobs[fid]["status"] == "PROCESSED"
    assert pipeline.jobs[fid]["size"] == len(b"raw_image_bytes")
