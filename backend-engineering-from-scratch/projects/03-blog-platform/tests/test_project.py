"""
Tests for Project: Relational Blog Platform
"""

import pytest
import os
import sys
import importlib.util

PROJ_DIR = os.path.dirname(os.path.abspath(__file__))
APP_FILE = os.path.join(os.path.dirname(PROJ_DIR), "app", "main.py")

spec = importlib.util.spec_from_file_location("proj_03_blog_platform", APP_FILE)
proj = importlib.util.module_from_spec(spec)
spec.loader.exec_module(proj)

globals().update({k: getattr(proj, k) for k in dir(proj) if not k.startswith("__")})

def test_blog_eager_loading():
    repo = BlogRepository()
    repo.create_post(1, "Post 1", "alice", ["backend", "sql"])
    repo.add_comment(1, 101, "Great article!")
    
    posts = repo.get_posts_eager()
    assert len(posts) == 1
    assert len(posts[0]["comments"]) == 1
    assert posts[0]["tags"] == ["backend", "sql"]
