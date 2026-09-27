# Part X: Environments & Configuration (Phases 70–74)

## Motto
> "An environment is an isolated runtime stage. Keep environments as similar as economically feasible, inject configuration from the outside, and protect production with explicit verification gates."

---

## Delivery Problem
A service functions flawlessly in Staging. When promoted to Production, database queries grind to a complete halt, causing widespread timeouts.

The root cause? In Staging, the database had 1,000 mock rows and ran on an unconstrained single node. In Production, the database held 50,000,000 rows across a sharded cluster with strict connection pooling and query timeouts. A missing database index that went unnoticed on small staging datasets caused a full table scan that took down production!

---

## Prediction
1. Lack of parity between staging and production hides performance bottlenecks and configuration errors.
2. Hardcoding environment endpoints in application code forces risky per-environment rebuilds.
3. CI environments with protection rules ensure that only reviewed, authorized changes reach production.

---

## First Principles
1. **The Twelve-Factor Configuration Principle**:
   An application's code and its configuration are strictly separated:
   - **Code**: Identical across all environments (packaged into the immutable artifact).
   - **Config**: Injected at runtime via environment variables (`DATABASE_URL`, `LOG_LEVEL`, `PORT`).
   - If changing an environment setting requires editing source code or recompiling the binary, Twelve-Factor principles are violated.
2. **Environment Parity**:
   Keep development, staging, and production as similar as economically feasible:
   - Same database engine (never use SQLite in dev and PostgreSQL in prod for complex queries).
   - Same OS runtime and container base image.
   - Same network topologies and ingress routing patterns.
3. **Gated Promotion**:
   Software moves sequentially across environment boundaries:
   `Ephemeral PR Environment ──► Staging ──► Production (Protected)`.

---

## Manual Process
Observe Twelve-Factor environment configuration manually:

```bash
# Run with Staging configuration
ENVIRONMENT=staging PORT=8081 python3 -c "
import os
print(f'Running in: {os.environ.get(\"ENVIRONMENT\")} on port {os.environ.get(\"PORT\")}')
"

# Run with Production configuration (Exact same code!)
ENVIRONMENT=production PORT=8080 python3 -c "
import os
print(f'Running in: {os.environ.get(\"ENVIRONMENT\")} on port {os.environ.get(\"PORT\")}')
"
```

---

## Mental Model

```text
[ Immutable Binary: delivery-service ]
                  │
        ┌─────────┴─────────┐
        ▼                   ▼
 [ Staging Node ]   [ Production Node ]
 - Injected Env:    - Injected Env:
   DB_URL=stg.db      DB_URL=prod.db
   LOG_LEVEL=DEBUG    LOG_LEVEL=WARN
   PORT=8081          PORT=8080
```

---

## Automate It (Phase 74: CI Deployment Environments & Protection Rules)

```yaml
# .github/workflows/production.yml
jobs:
  deploy-production:
    runs-on: ubuntu-24.04
    environment:
      name: production # Gated by manual reviewer approval & deployment windows (Phase 74)
      url: https://delivery-service.internal
    steps:
      - uses: actions/checkout@v4.1.7
      - run: bash scripts/test.sh
```

---

## Run It
Inspect environment variable bindings in `sample-apps/delivery-service/app.py`:
```bash
python3 -c "
from sample-apps.delivery-service.app import ENVIRONMENT, PORT 2>/dev/null || true
print('Configuration parsed from environment variables.')
"
```

---

## Break It (Phase 71: Environment Parity Failure)
1. Run broken lab `20-deploy-succeeds-but-app-crashes-on-startup`:
   ```bash
   python3 broken-pipelines/20-deploy-succeeds-but-app-crashes-on-startup/reproduce_failure.py
   ```
2. Run broken lab `37-environment-protection-rule-bypass-via-push`:
   ```bash
   python3 broken-pipelines/37-environment-protection-rule-bypass-via-push/reproduce_failure.py
   ```
3. Observe how missing required environment variables cause startup crashes on production.

---

## Debug It
When an application fails in production after passing staging:
- Compare environment variable names and formats between Staging and Production.
- Check if secrets were properly injected into the pod environment or if they resolved to empty strings.

---

## Security
- Store production secrets in a dedicated secret manager (AWS Secrets Manager, HashiCorp Vault).
- Restrict access to production environment secrets in CI so that normal PR jobs cannot read them.

---

## Optimize It
- Spin up ephemeral preview environments for pull requests (e.g. via KinD or ephemeral Kubernetes namespaces) and destroy them upon PR merge to optimize cloud spend.

---

## Deployment Implication
Gating production behind an environment protection rule ensures that deployment is an intentional, auditable action rather than an accidental side-effect of a feature push.

---

## Recovery
If a bad configuration is deployed:
- Fix the configuration in the secret manager or environment manifest; do not rebuild the application image.
- Restart pod replicas to pick up the updated environment configuration.

---

## Practical Exercises (Part X)
1. **Exercise 10.1**: Write a script that compares the keys in a `.env.staging` file against `.env.production` and flags missing keys.
2. **Exercise 10.2**: Configure GitHub Environment protection rules requiring two designated reviewers before a job can proceed.
3. **Exercise 10.3**: Implement a startup configuration validator in `app.py` that fails fast if `PORT` or `ENVIRONMENT` is missing.
4. **Exercise 10.4**: Simulate an ephemeral PR preview environment using Docker Compose and verify its automatic teardown.
5. **Exercise 10.5**: Test application behavior when `DATABASE_URL` points to an unreachable host and observe the readiness probe failure.
6. **Exercise 10.6**: Write a script that checks whether any sensitive credentials exist as plain text in deployment manifest files.
7. **Exercise 10.7**: Benchmark connection pooling differences between a single-connection staging database and a production pooled database.
8. **Exercise 10.8**: Implement a deployment schedule rule that prevents production deployments outside of business hours (e.g. Friday evenings).

---

## Questions for Mastery
1. *Why should an application never contain environment detection code like `if env == 'production': do_x()`?*
2. *How do GitHub Actions environment protection rules protect production secrets from being accessed by feature branch builds?*
3. *What are the economic and operational trade-offs of maintaining 100% staging-to-production parity?*

---

## What Comes Next
In **Part XI (Phases 75–83)**, we dive into Authentication & Pipeline Security: why CI credentials are high-risk targets, long-lived secrets vs OIDC Workload Identity, least privilege, fork PR boundaries, action pinning, and runner isolation.
