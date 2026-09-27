# Capstone 04: Production Readiness Review (PRR)

An automated Production Readiness Audit engine and health probe evaluator.
Enforces production-grade standards across 5 critical engineering pillars:
1. **Configuration & Secrets**: Validates non-default secrets, environment variable decoupling, and DB URI formatting.
2. **Health Probes**: Evaluates liveness (`/livez`) and readiness (`/readyz`) dependency health checks.
3. **Security Posture**: Checks CORS restrictions, security response headers (`HSTS`, `X-Content-Type-Options`), and rate limiting.
4. **Observability Readiness**: Audits structured JSON logging, RED metrics exposition, and correlation ID propagation.
5. **Resilience & SLAs**: Verifies timeout definitions and graceful termination hooks.

---

## 1. Audit Workflow

```text
Service Metadata & Config Dict
        │
        ▼
[Production Readiness Engine]
        ├── Check 1: Secrets & Env Variables
        ├── Check 2: Liveness & Readiness Probes
        ├── Check 3: Security Headers & CORS
        ├── Check 4: RED Metrics & Observability
        └── Check 5: Timeout Boundaries
        │
        ▼
[Readiness Report] ──▶ Score (0-100%) + Actionable Remediation Items
```

## 2. Running Tests
```bash
pytest apps/04_production_readiness_review/tests/ -v
```
