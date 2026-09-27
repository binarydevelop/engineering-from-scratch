# Phases 175 – 188: Building a Mini Platform from Scratch

> **Motto**: Understand it. Instrument it. Measure it. Break it. Detect it. Debug it. Recover it. Automate it. Improve it. Operate it.

---

## Phases 175 – 181: Service Scaffolding, CLI & Default Observability

### The Golden Path Service Scaffold (Phase 175)
The template in `platform/templates/service_template/` contains:
* `main.py`: Pre-configured FastAPI application with standard health endpoints (`/healthz`, `/ready`), OpenTelemetry SDK initialization, and Prometheus `/metrics`.
* `Dockerfile`: Hardened distroless multi-stage container build with graceful `SIGTERM` shutdown timeout.
* `service.yaml`: Clean declarative manifest declaring port, resource limits, and owning team.

### The Service Bootstrap CLI (Phase 176)
```bash
python3 platform/cli/main.py new-service \
  --name payment-audit \
  --team payments \
  --port 8085
```
Generates a complete, compliant microservice in under 3 seconds!

### Zero-Touch Observability Wiring (Phase 179)
When a service is bootstrapped:
1. `service.name` is injected into OpenTelemetry resource attributes.
2. Standard RED metrics (`http_requests_total`, `http_request_duration_seconds`) are wired to HTTP middleware automatically.
3. Prometheus scrape job is registered.
4. Grafana RED dashboard is automatically provisioned for that service name.

---

## Phases 182 – 188: Self-Service Backends, Catalogs & Scorecards

### Database-as-a-Service Lite (Phase 182)
Developers declare database dependencies in `service.yaml`:
```yaml
dependencies:
  - postgresql
```
The platform dynamically creates an isolated database tenant, generates least-privilege credentials, and injects the connection string into the container environment.

### The Software Catalog (Phase 185)
Maintained in `platform/catalog/services.yaml`:
* Tracks all services, owning teams, criticality tiers, ports, repository URLs, runbook links, and active dependencies.
* Inspect with `python3 platform/cli/main.py catalog`.

### Production Readiness Scorecards (Phase 186)
Automated PRR compliance evaluation:
```bash
python3 platform/cli/main.py scorecard --dir services/api-gateway
```
Evaluates 6 core invariants (health probes, metrics, structured logs, graceful shutdown, resource limits, ownership) and outputs a letter grade (`A`, `B`, `C`, `F`).
