# Solution: Broken Pipeline Lab 32 — Multi-Stage Build Copies Host Source Instead of Compiled Binary

## 1. Root Cause Analysis
`COPY --from=builder` had a typo (`COPY --from=build`) which silently fell back to copying from local host context.

---

## 2. Step-by-Step Fix
Ensure exact stage names match in `COPY --from=<stage_name>`.

---

## 3. Verification Command
To verify that the fix resolves the issue, run:
```bash
python3 broken-pipelines/32-multi-stage-docker-copies-from-wrong-stage/solution/verify_fix.py
```

---

## 4. Organizational Prevention Policy
> **Prevention Rule**: Enable Docker BuildKit (`DOCKER_BUILDKIT=1`) to enforce strict stage reference validation.
