# Solution: Broken Pipeline Lab 17 — Third-Party Action Tag Hijacked by Malicious Release

## 1. Root Cause Analysis
Action was referenced by mutable tag rather than immutable 40-character commit SHA.

---

## 2. Step-by-Step Fix
Pin action to immutable commit SHA: `uses: third-party/action@692973e3d9... # v1.4.2`.

---

## 3. Verification Command
To verify that the fix resolves the issue, run:
```bash
python3 broken-pipelines/17-unpinned-third-party-action-supply-chain-tamper/solution/verify_fix.py
```

---

## 4. Organizational Prevention Policy
> **Prevention Rule**: Enforce automated action pinning via linter (e.g. zizmor or pin-github-action).
