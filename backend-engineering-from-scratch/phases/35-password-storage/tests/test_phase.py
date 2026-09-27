"""
Test suite for Lesson 35: Password Storage.
"""

import pytest
import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
CODE_FILE = os.path.join(os.path.dirname(CURRENT_DIR), "code", "main.py")
mod_name = os.path.basename(os.path.dirname(CURRENT_DIR)).replace("-", "_")

import importlib.util
spec = importlib.util.spec_from_file_location(mod_name, CODE_FILE)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
globals().update({k: getattr(mod, k) for k in dir(mod) if not k.startswith("__")})

def test_password_hashing_and_verification():
    # Use 4 rounds for fast unit tests
    hasher = PasswordHasher(rounds=4)
    password = "CorrectHorseBatteryStaple123!"
    
    hashed = hasher.hash_password(password)
    assert hashed != password
    assert hashed.startswith("$2b$") or hashed.startswith("$2a$")

    # Correct password succeeds
    assert hasher.verify_password(password, hashed) is True

    # Incorrect password fails
    assert hasher.verify_password("WrongPassword", hashed) is False

def test_unique_salts_produce_different_hashes():
    hasher = PasswordHasher(rounds=4)
    password = "identical_password"
    
    hash1 = hasher.hash_password(password)
    hash2 = hasher.hash_password(password)
    
    # Even with identical password, salts must differ
    assert hash1 != hash2
    assert hasher.verify_password(password, hash1) is True
    assert hasher.verify_password(password, hash2) is True
