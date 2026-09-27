# Phases 158 – 165: Production Readiness & Toil Elimination

> **Motto**: Understand it. Instrument it. Measure it. Break it. Detect it. Debug it. Recover it. Automate it. Improve it. Operate it.

---

## Phase 158: The Production Readiness Review (PRR)

### Motto
"A service is not ready for production because its code compiles; it is ready when its failure modes are understood, observable, and recoverable."

### Reviewing Against `PRODUCTION_READINESS_TEMPLATE.md`
Before receiving production traffic, every service undergoes a PRR auditing:
1. **Ownership**: Named engineering team, on-call roster, Slack alerts channel.
2. **SLO Defined**: Documented SLI equation, 30-day target, error budget policy.
3. **Capacity & Headroom**: Load tested to 2x peak traffic; operates at $\le 60\%$ CPU.
4. **Health Probes**: Working `/healthz` (startup/liveness) and `/ready` (readiness).
5. **Telemetry**: OTel resource identity, structured JSON logs, RED metrics, W3C trace context.
6. **Alerts & Runbooks**: Symptom-based paging alerts linked to verified Markdown runbooks.
7. **Resilience**: Client timeouts, retries with jitter, circuit breakers on dependencies.
8. **Deployment Safety**: Zero-downtime rolling updates, verified one-command rollback.

---

## Phases 159 – 162: Service Ownership, Catalogs & Runbook Automation

### Operational Ownership (Phase 159)
The team that writes the service MUST operate the service. Throwing code over the wall to a separate operations team creates misaligned incentives where developers push risky code and operators suffer through midnight outages.

### Runbook Automation (Phase 162)
If a runbook says: *"Step 1: Check if consumer is lagging. Step 2: Restart pod."*  
**Automate it!** A script that executes reliably at 3 AM is strictly better than a human fumbling through shell commands on a smartphone.

---

## Phases 163 – 165: Measuring & Eliminating Operational Toil

### The 6 Characteristics of Toil
Work that is:
1. Manual
2. Repetitive
3. Automatable
4. Tactical / reactive
5. Low enduring value
6. Scales linearly as traffic grows

### The SRE 50% Rule
Google SRE caps operational toil at **50% of an engineer's time**. The remaining 50%+ MUST be spent on engineering projects that eliminate toil permanently (building platforms, automating rollbacks, redesigning architectures).
