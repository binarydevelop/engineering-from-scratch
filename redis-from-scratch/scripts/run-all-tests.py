#!/usr/bin/env python3
"""
scripts/run-all-tests.py — Automated verification and test runner for redis-from-scratch.
"""

import os
import sys
import glob
import py_compile
import subprocess

BOLD = "\033[1m"
GREEN = "\033[0;32m"
RED = "\033[0;31m"
YELLOW = "\033[0;33m"
RESET = "\033[0m"

def test_file_structure():
    print(f"\n{BOLD}1. Verifying Complete 51-Phase Structure (Phases 00 to 50)...{RESET}")
    base = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "phases"))
    phases = sorted(os.listdir(base))
    assert len(phases) == 51, f"Expected 51 phases, found {len(phases)}"
    
    missing = []
    for p in phases:
        p_dir = os.path.join(base, p)
        for sub in ["docs/en.md", "experiments/run_experiment.sh", "outputs/evidence-template.md"]:
            path = os.path.join(p_dir, sub)
            if not os.path.exists(path):
                missing.append(path)
        # Check code dir has at least one python script
        code_files = glob.glob(os.path.join(p_dir, "code", "*.py"))
        if not code_files:
            missing.append(f"{p_dir}/code/*.py")

    if missing:
        print(f"  [{RED}FAIL{RESET}] Missing components in phases: {missing}")
        return False
    print(f"  [{GREEN}PASS{RESET}] All 51 phases contain valid docs/en.md, code, experiments, and outputs.")
    return True

def test_python_syntax():
    print(f"\n{BOLD}2. Compiling and Verifying Syntax of All Python Code...{RESET}")
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    py_files = []
    for root, _, files in os.walk(repo_root):
        if ".git" in root or "__pycache__" in root or ".venv" in root: continue
        for f in files:
            if f.endswith(".py"):
                py_files.append(os.path.join(root, f))
    
    errors = 0
    for pf in py_files:
        try:
            py_compile.compile(pf, doraise=True)
        except py_compile.PyCompileError as e:
            print(f"  [{RED}ERROR{RESET}] Syntax error in {pf}: {e}")
            errors += 1
    
    if errors == 0:
        print(f"  [{GREEN}PASS{RESET}] Successfully compiled {len(py_files)} Python scripts with zero syntax errors.")
        return True
    return False

def test_unit_logic():
    print(f"\n{BOLD}3. Executing Unit Logic Tests for First-Principles Algorithms...{RESET}")
    
    # Test 1: MiniKV (Phase 02)
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "phases", "02-build-a-tiny-key-value-store", "code")))
    from mini_kv import MiniKV
    kv = MiniKV()
    assert kv.set("k1", "v1") == "OK"
    assert kv.get("k1") == "v1"
    assert kv.exists("k1") == 1
    assert kv.delete("k1") == 1
    assert kv.get("k1") is None
    print(f"  [{GREEN}PASS{RESET}] Phase 02 MiniKV logic verified.")

    # Test 2: RESP Codec (Phase 04)
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "phases", "04-redis-protocol-resp", "code")))
    from resp_codec import encode_resp_command, decode_resp
    raw = encode_resp_command("PING")
    assert raw == b"*1\r\n$4\r\nPING\r\n"
    typ, val = decode_resp(b"+PONG\r\n")
    assert typ == "SimpleString" and val == "PONG"
    print(f"  [{GREEN}PASS{RESET}] Phase 04 RESP Serialization logic verified.")

    # Test 3: LRU Cache (Phase 14)
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "phases", "14-lru-and-lfu-from-scratch", "code")))
    from lru_lfu_scratch import ExactLRUCache
    lru = ExactLRUCache(2)
    lru.put("a", 1); lru.put("b", 2)
    lru.get("a") # access a -> b becomes oldest
    lru.put("c", 3) # evicts b
    assert "b" not in lru.cache
    assert "a" in lru.cache and "c" in lru.cache
    print(f"  [{GREEN}PASS{RESET}] Phase 14 LRU Cache eviction logic verified.")

    # Test 4: Cluster Hash Slot & Hash Tags (Phase 38)
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "phases", "38-redis-cluster", "code")))
    from cluster_slots import get_slot
    s1 = get_slot("{user:42}:orders")
    s2 = get_slot("{user:42}:profile")
    assert s1 == s2, f"Expected matching slots, got {s1} and {s2}"
    print(f"  [{GREEN}PASS{RESET}] Phase 38 Cluster Hash Tag colocation verified.")

    return True

def main():
    print(f"{BOLD}================================================================{RESET}")
    print(f"{BOLD}       redis-from-scratch — Automated Test & Validation         {RESET}")
    print(f"{BOLD}================================================================{RESET}")
    
    t1 = test_file_structure()
    t2 = test_python_syntax()
    t3 = test_unit_logic()

    print(f"\n{BOLD}----------------------------------------------------------------{RESET}")
    if t1 and t2 and t3:
        print(f"{GREEN}{BOLD}✓ ALL VERIFICATION CHECKS PASSED SUCCESSFULLY!{RESET}\n")
        sys.exit(0)
    else:
        print(f"{RED}{BOLD}✗ VERIFICATION FAILED.{RESET}\n")
        sys.exit(1)

if __name__ == "__main__":
    main()
