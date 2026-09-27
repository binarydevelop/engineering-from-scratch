#!/usr/bin/env python3
"""
Updates all `test_phase.py` in `phases/` to use `importlib.util.spec_from_file_location`
with unique module names. This prevents pytest module caching collisions where
`sys.modules['main']` retains the first phase's `main.py` across different test files.
"""

import os
import glob
import re

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PHASES_DIR = os.path.join(REPO_ROOT, "phases")

def update_test_file(test_path: str):
    with open(test_path, "r", encoding="utf-8") as f:
        content = f.read()

    # If already using importlib loader, skip
    if "spec_from_file_location" in content:
        return

    replacement = """CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
CODE_FILE = os.path.join(os.path.dirname(CURRENT_DIR), "code", "main.py")
mod_name = os.path.basename(os.path.dirname(CURRENT_DIR)).replace("-", "_")

import importlib.util
spec = importlib.util.spec_from_file_location(mod_name, CODE_FILE)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
globals().update({k: getattr(mod, k) for k in dir(mod) if not k.startswith("__")})"""

    # Match the old import block:
    # Optional comment
    # CURRENT_DIR = ...
    # CODE_DIR = ...
    # if CODE_DIR not in sys.path:
    #     sys.path.insert(0, CODE_DIR)
    # from main import ...
    pattern = r"(?:# Ensure code directory is in path\s*\n)?CURRENT_DIR = os\.path\.dirname\(os\.path\.abspath\(__file__\)\)\s*\nCODE_DIR = os\.path\.join\(os\.path\.dirname\(CURRENT_DIR\), \"code\"\)\s*\nif CODE_DIR not in sys\.path:\s*\n\s*sys\.path\.insert\(0, CODE_DIR\)\s*\n\s*from main import [^\n]+"

    new_content, n = re.subn(pattern, replacement, content)
    if n > 0:
        with open(test_path, "w", encoding="utf-8") as f:
            f.write(new_content)
    else:
        print(f"Warning: pattern not matched in {test_path}")

def main():
    test_files = sorted(glob.glob(os.path.join(PHASES_DIR, "*", "tests", "test_phase.py")))
    print(f"Found {len(test_files)} test_phase.py files. Updating...")
    for tf in test_files:
        update_test_file(tf)
    print("All test_phase.py files processed successfully!")

if __name__ == "__main__":
    main()
