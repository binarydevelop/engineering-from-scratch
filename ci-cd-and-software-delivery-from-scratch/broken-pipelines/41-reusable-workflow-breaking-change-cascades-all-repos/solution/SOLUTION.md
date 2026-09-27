# Solution: Broken Pipeline Lab 41 — Unversioned Reusable Workflow Change Breaks 40 Downstream Repos

## 1. Root Cause Analysis
Repositories referenced reusable workflow via `@main` instead of pinned semantic versions (`@v1`, `@v2`).

---

## 2. Step-by-Step Fix
Pin downstream repositories to immutable semantic version tags or SHAs.

---

## 3. Verification Command
To verify that the fix resolves the issue, run:
```bash
python3 broken-pipelines/41-reusable-workflow-breaking-change-cascades-all-repos/solution/verify_fix.py
```

---

## 4. Organizational Prevention Policy
> **Prevention Rule**: Version reusable platform workflows with deprecation lifecycles and semantic versioning.
