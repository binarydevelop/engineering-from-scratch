# Solution: Broken Pipeline Lab 35 — Secret Scanner Bypassed by Base64 Encoded Token

## 1. Root Cause Analysis
Scanner only looked for plain string prefixes like `AKIA...`.

---

## 2. Step-by-Step Fix
Use entropy-based and multi-encoding secret scanners (e.g. TruffleHog, Trivy).

---

## 3. Verification Command
To verify that the fix resolves the issue, run:
```bash
python3 broken-pipelines/35-secret-scanning-regex-bypass/solution/verify_fix.py
```

---

## 4. Organizational Prevention Policy
> **Prevention Rule**: Combine pattern-based scanning with high-entropy heuristic analysis.
