"""
Tests for Project: Todo Task Management API
"""

import pytest
import os
import sys
import importlib.util

PROJ_DIR = os.path.dirname(os.path.abspath(__file__))
APP_FILE = os.path.join(os.path.dirname(PROJ_DIR), "app", "main.py")

spec = importlib.util.spec_from_file_location("proj_02_todo_api", APP_FILE)
proj = importlib.util.module_from_spec(spec)
spec.loader.exec_module(proj)

globals().update({k: getattr(proj, k) for k in dir(proj) if not k.startswith("__")})

def test_task_lifecycle_and_ownership():
    service = TaskService()
    t1 = service.create("user_a", "Buy groceries")
    assert t1["completed"] is False

    # Owner can complete
    completed = service.complete("user_a", t1["id"])
    assert completed["completed"] is True

    # Other user cannot access
    import pytest
    with pytest.raises(PermissionError):
        service.complete("user_b", t1["id"])
