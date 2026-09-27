# Part XIV — AI Observability & Tracing (Phases 175 – 180)

> **Motto:** If you cannot trace where tokens, dollars, and milliseconds are spent, you cannot operate an AI system.

---

## Phases 175 – 180: Tracing, Cost Accounting & Diagnostic Taxonomies
- **Phase 175 — Tracing an Agent Run:** End-to-end distributed tracing: tracking prompts, tools, latencies, and token counts.
- **Phase 176 — Structured AI Traces:** Emitting OpenTelemetry-compatible spans for model invocations and tool actions.
- **Phase 177 — Token Cost & Budget Accounting:** Real-time dollar metering of input, output, and cache tokens per tenant.
- **Phase 178 — Quality Monitoring Beyond HTTP 200:** Monitoring semantic correctness, schema failure rates, and drift in production.
- **Phase 179 — Agent Failure Taxonomy:** Structured categorization of production failures (model, tool, schema, timeout, policy).
- **Phase 180 — Root-Cause Debugging:** Step-by-step diagnostic workflow: isolating whether failure is model, data, tool, or code (`docs/troubleshooting.md`).
