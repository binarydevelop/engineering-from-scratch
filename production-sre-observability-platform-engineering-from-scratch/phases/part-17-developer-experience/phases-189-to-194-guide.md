# Phases 189 – 194: Developer Experience & Friction Elimination

> **Motto**: Understand it. Instrument it. Measure it. Break it. Detect it. Debug it. Recover it. Automate it. Improve it. Operate it.

---

## Phases 189 – 191: Cognitive Load, TTFD & Local Dev

### Measuring Cognitive Load (Phase 189)
Count the distinct conceptual domains an engineer must know to deploy a simple HTTP endpoint:
* **High Friction Stack**: Git, Dockerfile syntax, Linux cgroups, Kubernetes Deployment, Service, Ingress, Cert-Manager, Helm values, Prometheus annotations, OpenTelemetry OTLP URLs, Vault token renewal (11 distinct domains!).
* **Golden Path Platform**: Git commit + `service.yaml` (2 domains).
The platform eliminates the 9 incidental domains while keeping the runtime observable.

### Time to First Deploy (TTFD) (Phase 190)
Measure onboarding friction:
1. Clone repository.
2. Run `platform new-service`.
3. Push to branch.
4. Verify that CI builds, deploys to ephemeral staging, and passes health checks in $< 10\text{ minutes}$.

---

## Phases 192 – 194: Previews, Documentation & Support Auditing

### Ephemeral Preview Environments (Phase 192)
Every GitHub Pull Request spins up an isolated ephemeral environment (Docker Compose or disposable K8s namespace). Developers test changes under live conditions and teardown occurs automatically on PR merge.

### Platform Support Burden as Product Signal (Phase 194)
If developers file 50 Jira tickets a month asking *"How do I connect my service to Prometheus?"*, **this is not user error—it is a platform usability failure**.
Use support ticket trends as the primary backlog driver for platform improvements.
