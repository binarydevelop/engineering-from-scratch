# Platform Capability Design Document

> **Motto**: The internal developer platform is a product; developers are its demanding customers. If the platform is not significantly easier and more reliable than doing it manually, developers will build shadow IT.

---

# Platform Capability
[Name of capability, e.g. "Automated Self-Service Microservice Provisioning & Baseline Telemetry (`platform new-service`)"]

## Developer User
[Who is the customer? E.g., Product backend software engineers building new microservices, background workers, or event consumers.]

## Problem
[Describe the pain point: E.g., Creating a new production-ready microservice requires 3 days of manual copy-pasting of Dockerfiles, Kubernetes manifests, OpenTelemetry boilerplate, Prometheus scrape annotations, CI/CD pipelines, and secret vault configurations. Configurations diverge, leading to missing logs, broken traces, and unmonitored services.]

## Current Workflow
[Step-by-step description of how engineers solve this today without the platform capability, including manual tickets to DevOps/Infra.]

## Baseline Cost / Friction
* **Time to First Deploy**: 3-5 business days.
* **Support Ticket Burden**: 12 Jira tickets/month per team regarding broken CI or missing metrics.
* **Configuration Drift**: 40% of microservices lack standard resource limits or graceful shutdown logic.

## Desired Outcome
* A single CLI command creates a fully compliant, observable, and deployable service skeleton in under 3 minutes.
* Automated CI, telemetry pipeline integration, and health endpoints work out-of-the-box.

## Platform Interface
[Declarative YAML or CLI contract presented to the developer]
```bash
platform new-service \
  --name order-processing \
  --tier tier-1 \
  --team checkout \
  --port 8080 \
  --with-postgres \
  --with-redis
```
Or declarative manifest `service.yaml`:
```yaml
apiVersion: platform.internal/v1alpha1
kind: Service
metadata:
  name: order-processing
  team: checkout
spec:
  port: 8080
  tier: 1
  resources:
    profile: standard-api # 500m CPU, 512Mi Memory
  dependencies:
    - postgresql
    - redis
```

## Responsibilities

### Platform owns
* Telemetry infrastructure: OTel Collector routing, Prometheus scrape configuration, Loki/Tempo ingestion.
* Base container images, security hardening, and distroless runtimes.
* CI/CD pipeline automation and automated canary deployment controllers.
* Secret injection mechanism and database provisioning orchestration.

### Service team owns
* Application business logic and domain correctness.
* Definition of custom SLI equations and business SLO targets.
* High-value application domain instrumentation and span attributes.
* Production incident response and service-specific operational runbooks.

## Golden Path
[The opinionated, supported, lowest-friction default path that solves 80% of use cases]
1. Run `platform new-service`.
2. Commit code to Git.
3. CI automatically runs tests, builds OCI container, and deploys to staging with baseline Grafana RED dashboard automatically provisioned.

## Escape Hatch
[Deliberate mechanism for teams with unique requirements, e.g. custom C++ runtimes or specialized GPU hardware]
* Teams can eject or override generated Kubernetes manifests via `platform eject-manifests`.
* Custom Dockerfiles supported with verified platform base image compliance tests.

## Guardrails
* Mandatory linter verifies presence of `/healthz`, `/ready`, and graceful `SIGTERM` handler.
* Policy enforcement (Open Policy Agent / Kyverno) blocks deployments without CPU/Memory limits.

## Adoption Plan
* Phase 1: Pilot with 2 founding product teams.
* Phase 2: Incorporate feedback and publish golden path guide.
* Phase 3: Deprecate manual legacy deployment templates.

## Success Metrics
* **Time to First Deploy**: < 10 minutes (down from 3 days).
* **Golden Path Adoption**: >= 85% of all new services within 6 months.
* **Telemetry Compliance**: 100% of new services reporting valid RED metrics and trace context on day 1.

## Support Model
* Dedicated Slack channel `#platform-help`.
* Self-service interactive troubleshooting guides and task-oriented documentation.

## Feedback Loop
* Monthly Net Promoter Score (NPS) developer survey.
* Weekly review of platform build logs, error rates, and support tickets to identify friction.
