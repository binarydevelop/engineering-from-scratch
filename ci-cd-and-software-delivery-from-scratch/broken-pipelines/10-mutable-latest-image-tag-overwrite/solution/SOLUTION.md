# Solution: Broken Pipeline Lab 10 — Production Pulls Unexpected Code Due to Overwritten 'latest' Tag

## 1. Root Cause Analysis
Deployments targeted mutable tag `:latest` instead of immutable digest (`@sha256:...`) or unique release tag (`:v1.2.0`).

---

## 2. Step-by-Step Fix
Pin Kubernetes manifests to immutable content digests (`image@sha256:7f9b...`).

---

## 3. Verification Command
To verify that the fix resolves the issue, run:
```bash
python3 broken-pipelines/10-mutable-latest-image-tag-overwrite/solution/verify_fix.py
```

---

## 4. Organizational Prevention Policy
> **Prevention Rule**: Configure container registries to make release tags immutable and disallow overwriting.
