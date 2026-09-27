# Platform Engineering: Golden Paths & Developer Experience

> **Motto**: The goal of platform engineering is not to build a bureaucracy of YAML generators; it is to reduce cognitive load and make reliable operations the default path of least resistance.

---

## 1. The Core Purpose: Reducing Incidental Cognitive Load

In modern engineering organizations, software developers are burdened by an explosion of infrastructure tooling:

```text
Without a Platform (Incidental Cognitive Load):
Developer -> Git -> Dockerfile -> Helm Charts -> K8s YAMLs -> Prometheus Rules -> OTel Config -> Secret Vault -> CI Scripts -> Cloud IAM

With a Golden Path (Focus on Domain Logic):
Developer -> platform new-service -> service.yaml (15 lines) -> Production-Ready Observable System
```

---

## 2. The Five Laws of Platform Engineering

1. **Platform as a Product**: Internal developers are users. Conduct user research, track developer NPS, and measure Time to First Deploy (TTFD).
2. **Golden Paths, Not Mandatory Prisons**: Make the standard path so easy, fast, and reliable that 80%+ of teams choose it voluntarily. Always provide an explicit escape hatch for specialized architectures.
3. **Never Hide Essential Operational Truths**: An abstraction that hides how Kubernetes schedules containers or how TCP connections pool makes production unknowable. Developers must be able to peel back the layer during an outage.
4. **Self-Service Means Zero Tickets**: If provisioning a database requires filing a Jira ticket to an infrastructure team, it is not self-service.
5. **Guardrails Over Gates**: Enforce security, resource limits, and telemetry compliance via automated CI linters and admission controllers, not manual human approval boards.

---

## 3. Platform Capabilities vs Application Ownership

```text
┌──────────────────────────────────────────────┬──────────────────────────────────────────────┐
│ Platform Team Guarantees                     │ Application Service Team Owns                │
├──────────────────────────────────────────────┼──────────────────────────────────────────────┤
│ - OTel Collector telemetry routing pipeline  │ - Domain business logic and error handling   │
│ - Base container images & security scanning  │ - Application-specific SLI/SLO targets       │
│ - Self-service database/queue provisioning   │ - Schema design, migrations, and query tuning│
│ - Standardized CI/CD build & deploy runners  │ - Incident triage for business exceptions    │
│ - Default RED/USE Grafana dashboard templates│ - Operational runbooks for service alerts    │
└──────────────────────────────────────────────┴──────────────────────────────────────────────┘
```
