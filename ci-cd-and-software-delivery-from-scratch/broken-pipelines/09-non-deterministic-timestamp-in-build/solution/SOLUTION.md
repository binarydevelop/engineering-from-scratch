# Solution: Broken Pipeline Lab 09 — Embedded Wall-Clock Timestamp Prevents Build Reproducibility

## 1. Root Cause Analysis
The packaging step embedded current date/time into the archive header and compiled binary.

---

## 2. Step-by-Step Fix
Clamp build timestamps to `SOURCE_DATE_EPOCH` derived from the last Git commit timestamp.

---

## 3. Verification Command
To verify that the fix resolves the issue, run:
```bash
python3 broken-pipelines/09-non-deterministic-timestamp-in-build/solution/verify_fix.py
```

---

## 4. Organizational Prevention Policy
> **Prevention Rule**: Validate bit-for-bit reproducibility in release pipelines using diffoscope or hash comparisons.
