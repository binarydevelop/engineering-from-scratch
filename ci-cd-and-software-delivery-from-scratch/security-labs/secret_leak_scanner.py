#!/usr/bin/env python3
"""
Secret Leak Scanner (Phase 41, 199)
Detects committed secrets, tokens, API keys, and private certificates before they reach Git or CI logs.
"""

import argparse
import os
import re
import sys
from typing import List, Tuple

# Patterns for high-risk credentials
SECRET_PATTERNS = [
    ("AWS Access Key ID", re.compile(r"(A3T[A-Z0-9]|AKIA|AGPA|AIDA|AROA|AIPA|ANPA|ANVA|ASIA)[A-Z0-9]{16}")),
    ("GitHub Personal Access Token", re.compile(r"gh[pousr]_[A-Za-z0-9_]{36,255}")),
    ("Generic Private Key", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----")),
    ("Slack API Token", re.compile(r"xox[baprs]-[0-9a-zA-Z]{10,48}")),
    ("Hardcoded Password in Code", re.compile(r"(?i)(password|secret|api_key|token)\s*=\s*['\"][a-zA-Z0-9!@#$%^&*()_+]{8,}['\"]")),
]

IGNORE_DIRS = {".git", ".venv", "venv", "__pycache__", "reports", ".pytest_cache", "outputs"}


def scan_file(filepath: str) -> List[Tuple[int, str, str]]:
    findings = []
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            for line_no, line in enumerate(f, 1):
                # Allow intentional testing comments that mark lines as safe
                if "nosec" in line.lower() or "safe-demo-secret" in line:
                    continue
                for name, pattern in SECRET_PATTERNS:
                    match = pattern.search(line)
                    if match:
                        findings.append((line_no, name, match.group(0)))
    except Exception as e:
        pass
    return findings


def scan_directory(directory: str) -> int:
    total_findings = 0
    print(f"Scanning directory: {directory} for secret leaks...")
    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        for file in files:
            filepath = os.path.join(root, file)
            # Skip binary and archive files
            if file.endswith((".tar.gz", ".whl", ".pyc", ".db", ".png", ".jpg")):
                continue
            findings = scan_file(filepath)
            if findings:
                for line_no, name, match in findings:
                    masked = match[:4] + "*" * (len(match) - 6) + match[-2:] if len(match) > 6 else "***"
                    print(f"  [CRITICAL LEAK] {filepath}:{line_no} - {name} detected: {masked}", file=sys.stderr)
                    total_findings += 1
    return total_findings


def main():
    parser = argparse.ArgumentParser(description="Static Secret Leak Scanner")
    parser.add_argument("--scan-dir", default=".", help="Directory to scan")
    args = parser.parse_args()

    leaks = scan_directory(args.scan_dir)
    if leaks > 0:
        print(f"\n✗ Scanner failed: {leaks} secret leak(s) detected. Fix before committing/deploying!", file=sys.stderr)
        sys.exit(1)
    else:
        print("✓ No secret leaks detected.")
        sys.exit(0)


if __name__ == "__main__":
    main()
