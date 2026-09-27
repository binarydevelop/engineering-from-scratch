# Solution: Broken Pipeline Lab 36 — Kubernetes YAML Valid YAML But Rejected by API Server

## 1. Root Cause Analysis
YAML syntax validator only proved syntactic correctness, not schema conformity against Kubernetes API schema.

---

## 2. Step-by-Step Fix
Validate manifests with `kubeconform` or `kubectl --dry-run=client` against target Kubernetes schema.

---

## 3. Verification Command
To verify that the fix resolves the issue, run:
```bash
python3 broken-pipelines/36-iac-manifest-syntax-valid-but-semantically-rejected/solution/verify_fix.py
```

---

## 4. Organizational Prevention Policy
> **Prevention Rule**: Integrate schema-aware linters into manifest validation pipelines.
