# Part XIX — Capstones & Final Enterprise Challenge (Phases 223 – 230)

> **Motto:** AI systems are no longer a model hidden behind an API call. Operate the complete converged stack under production constraints.

---

## The 8 Production Capstones

- **Phase 223 — Capstone 1: Compile and Serve a Model:** Compiling, quantizing, and load-testing a model with latency profiling.
- **Phase 224 — Capstone 2: Local Fine-Tuning Platform:** End-to-end CLI for dataset validation, LoRA training, checkpointing, and evals.
- **Phase 225 — Capstone 3: Production Agent Platform:** Production API gateway, auth, rate limiting, tracing, and sandboxed tools.
- **Phase 226 — Capstone 4: Fine-Tuned Agent:** Identifying a model tool-calling flaw, training an adapter, and proving improvement on eval suites.
- **Phase 227 — Capstone 5: Optimized Fine-Tuned Agent (`capstones/capstone05_integrated_ai_system.py`):** Complete convergence: LoRA model + optimized serving + sandboxed agent + OpenTelemetry tracing.
- **Phase 228 — Capstone 6: Failure Day (Chaos Engineering) (`capstones/capstone06_failure_day.py`):** Injected chaos across 12 production failure modes: outages, stale indexes, injections, and recovery.
- **Phase 229 — Capstone 7: Cost Reduction Engine (`capstones/capstone07_cost_reduction.py`):** Reducing production AI expenses by 70% while protecting benchmark quality through prompt pruning and model routing.
- **Phase 230 — Final AI Systems Challenge (`capstones/capstone08_final_enterprise_challenge.py`):**
  > *Build an enterprise AI assistant that answers questions over private company knowledge, performs selected actions, supports thousands of users, learns a domain-specific behavior style, and must satisfy strict latency, security, quality, and cost requirements.*
  >
  > The learner must independently reason through:
  > `requirements -> baseline eval -> model selection -> prompting vs retrieval vs fine-tuning -> dataset -> fine-tuning -> inference architecture -> compiler/runtime optimization -> retrieval -> agent/tool architecture -> permissions -> state/memory -> security -> observability -> evaluation -> load testing -> deployment -> failure recovery -> cost`.
