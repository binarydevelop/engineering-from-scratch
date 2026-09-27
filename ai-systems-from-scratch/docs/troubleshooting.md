# The Broken-AI Debugging & Troubleshooting Framework

> **Motto:** When an AI system fails, never immediately rewrite the prompt. Isolate the responsible layer through methodical causality tracing.

---

## 1. The 10-Step Failure Isolation Diagnostic Flow

```text
               User observes bad / inaccurate / failed output
                                     │
                                     ▼
 1. Was the raw user intent captured accurately by the interface?
    └─► NO: Fix input sanitation, voice-to-text, or UI encoding.
    └─► YES ──► Continue
                 │
                 ▼
 2. Was the necessary knowledge context present in the prompt window?
    └─► NO: Check Retrieval / RAG pipeline:
             ├─ Did the retrieval query miss the relevant chunks?
             ├─ Were retrieved chunks truncated by context window limits?
             └─ Did metadata filtering drop relevant tenant documents?
    └─► YES ──► Continue
                 │
                 ▼
 3. Was the prompt formatting / chat template valid for this model?
    └─► NO: Check special tokens (`<|start_header_id|>`, ChatML tokens).
    └─► YES ──► Continue
                 │
                 ▼
 4. Did the model make the correct action or tool decision?
    └─► NO: Tool selection failure. Check tool descriptions and few-shot examples.
    └─► YES ──► Continue
                 │
                 ▼
 5. Were tool arguments serialized in valid JSON matching the schema?
    └─► NO: Schema validation error. Introduce Pydantic grammar masking or retry.
    └─► YES ──► Continue
                 │
                 ▼
 6. Did the tool execution succeed without timeouts or 5xx exceptions?
    └─► NO: Tool infrastructure failure. Inspect tool server, DB logs, or timeouts.
    └─► YES ──► Continue
                 │
                 ▼
 7. Was the tool return payload within the model's processing budget?
    └─► NO: Tool payload overflow. Truncate, filter, or summarize tool output.
    └─► YES ──► Continue
                 │
                 ▼
 8. Did the model interpret the tool return value correctly?
    └─► NO: Model hallucinated or inverted tool output. Fine-tune or add rubric.
    └─► YES ──► Continue
                 │
                 ▼
 9. Did the agent / FSM workflow transition to the proper next state?
    └─► NO: State machine bug. Inspect transition table or scratchpad memory.
    └─► YES ──► Continue
                 │
                 ▼
10. Did serving / compilation corrupt numerical precision or token decoding?
    └─► Inspect FP16 underflow, temperature sampling, or KV cache corruption.
```

---

## 2. Common Anti-Patterns & Diagnoses

| Symptom | Intuitive (Wrong) Reaction | True Engineering Diagnosis & Fix |
| :--- | :--- | :--- |
| **"Model gives wrong policy answers"** | Rewrite the system prompt 10 times | Inspect RAG recall: Did the vector search fetch the latest 2026 policy document? |
| **"Agent hangs and runs up huge bill"** | Complain the model is dumb | Missing circuit breaker: Implement `MAX_AGENT_TURNS=10` and loop detection hash. |
| **"`torch.compile` is 3x slower"** | "Compilers don't work for PyTorch" | Inspect graph breaks: A Python `print()` or dynamic `len()` is causing 50 recompilations. |
| **"Triton kernel outputs NaNs"** | Blame hardware driver | Check boundary masking: Out-of-bounds pointer reads in block loading. |
| **"LoRA fine-tuning loss is 0.001 but eval is 0%"** | Celebrate training loss | Severe train/val contamination or label leakage in instruction formatting. |
| **"Double charge on credit card"** | Tell agent "Don't charge twice" | Missing idempotency key: Wrap payment tool in an atomic idempotency token store. |
