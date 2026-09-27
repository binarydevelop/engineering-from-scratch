# Part XVII — Broken AI Systems (Phases 195 – 207)

> **Motto:** You do not understand an AI system until you have broken it, observed its signature, and debugged it.

---

## Phases 195 – 206: The 12 Foundational Failure Labs
- **Phase 195 — Broken Compiler Lab:** Diagnosing why `torch.compile` runs slower than eager execution (graph breaks, warmup).
- **Phase 196 — Broken Kernel Lab:** Debugging a Triton kernel that runs fast but produces catastrophic numerical inaccuracy.
- **Phase 197 — Broken Fine-Tune Lab:** Diagnosing training loss collapse accompanied by validation loss explosion.
- **Phase 198 — Broken LoRA Lab:** Debugging an adapter that trains without error but produces zero behavioral change.
- **Phase 199 — Broken Quantization Lab:** Investigating why INT4 quantization destroyed reasoning on mathematical tasks.
- **Phase 200 — Broken Serving Lab:** Diagnosing why p99 latency spiked 50x under concurrent continuous batching.
- **Phase 201 — Broken Retrieval Lab:** Uncovering why a RAG agent hallucinated when retrieval fetched irrelevant noise.
- **Phase 202 — Broken Agent Tool Lab:** Debugging an agent generating invalid JSON parameters despite clear docstrings.
- **Phase 203 — Broken Agent Loop Lab:** Rescuing an agent stuck in an infinite tool-calling loop burning API budget.
- **Phase 204 — Broken Security Lab:** Exploiting and fixing an indirect prompt injection in a customer support workflow.
- **Phase 205 — Duplicate Side-Effect Lab:** Debugging a payment tool that billed a customer twice after a network retry.
- **Phase 206 — Context Explosion Lab:** Debugging a multi-turn conversation that crashed the inference engine with an OOM.

---

## Phase 207 — Master Broken AI Systems Set (40+ Labs)
- Complete diagnostic suite spanning 40 isolated defects across compilers, kernels, training, fine-tuning, serving, retrieval, agent loops, and security.
- **Interactive Diagnostic Runner:** Run `python broken-systems/run_all_diagnostics.py` to test and debug all 40 labs.
- **Solutions & Guides:** Complete implementations and root cause explanations stored in `broken-systems/solutions/solutions_implementation.py`.
