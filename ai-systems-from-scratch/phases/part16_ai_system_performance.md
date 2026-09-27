# Part XVI — End-to-End AI System Performance (Phases 187 – 194)

> **Motto:** Optimization without an end-to-end latency budget is premature. Measure every hop from user request to generated token.

---

## Phases 187 – 194: Latency Budgets, Economics & Serving Adapters
- **Phase 187 — End-to-End Latency Budgeting:** Allocating budgets: network, retrieval, TTFT, generation, tool calls.
- **Phase 188 — Token Economics:** Analyzing the marginal latency, dollar, and memory costs of bloated prompts.
- **Phase 189 — Context Optimization:** Pruning extraneous instructions and examples to optimize cost and latency.
- **Phase 190 — Model Size Tradeoffs:** Quantifying 1B vs 7B vs 70B across accuracy, TTFT, throughput, and hardware costs.
- **Phase 191 — Fine-Tuning vs Prompting vs RAG:** The ultimate comparison: evaluating all three on the exact same domain task (`experiments/finetune_vs_rag_vs_prompt.py`).
- **Phase 192 — Fine-Tuned Small Model vs Frontier Model:** Benchmarking a 3B domain LoRA model against a generic frontier model.
- **Phase 193 — Serving Fine-Tuned Adapters:** Latency and memory benchmarks of loading LoRA adapters dynamically at serving time.
- **Phase 194 — Multi-Tenant Adapter Serving:** Routing requests to hundreds of customer LoRA adapters on shared base weights.
