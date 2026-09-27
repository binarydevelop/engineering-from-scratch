# The AI Systems Engineering Learning Methodology

> **Repository Motto:**  
> **Understand it. Build it. Train it. Compile it. Serve it. Evaluate it. Break it. Debug it. Optimize it. Operate it.**

---

## 1. The Core Philosophy

This is not a course in prompt writing, and it is not a guided tour of Python SDK wrappers.  
**AI Systems Engineering is the discipline of adapting, optimizing, serving, orchestrating, evaluating, securing, and operating probabilistic models inside reliable software systems.**

When a system fails in production, you cannot fix it by randomly changing adjectives in your prompt or swapping high-level libraries. You must be able to trace execution from the highest orchestration layer down to the underlying memory bus:

```text
user request
  ↓
agent runtime & state
  ↓
prompt / message formatting
  ↓
tokenizer
  ↓
model forward pass
  ↓
compiled / optimized graph execution
  ↓
GPU memory & fused kernels
  ↓
autoregressive token generation
  ↓
tool call selection & schema validation
  ↓
tool execution & sandboxed state mutation
  ↓
state update & context management
  ↓
next model invocation
  ↓
tracing, evaluation & response
```

---

## 2. The 11 Iron Commandments of the Learner

1. **Predict Tensor Shapes Before Executing:** Before running any tensor operation, write down its input shape, output shape, element count, and memory footprint in bytes.
2. **Inspect Generated Graphs:** Never call `torch.compile` without inspecting the captured FX graph, checking for graph breaks, and understanding what inductor fused.
3. **Benchmark Rigorously:** Never report single-run latencies. Always separate warmup from steady-state, record median and p95/p99 percentiles, and state input/output sequence lengths.
4. **Verify Numerical Correctness:** Fast wrong kernels are still wrong. Verify custom operations against FP32 ground truth within strict numerical tolerances (`torch.allclose`).
5. **Account for Training & Serving Memory:** Calculate exact theoretical memory for model weights, gradients, optimizer states, KV cache, and activations before running out of memory.
6. **Implement the Loop Manually First:** Build the manual training loop (`forward -> loss -> backward -> step -> zero_grad`) and manual agent `while` loop before touching Hugging Face Trainer, LangChain, or agent SDKs.
7. **Inspect Datasets Manually:** Look at raw records, calculate token distributions, check for contamination between train and test splits, and inspect chat templates.
8. **Evaluate Before and After Every Change:** Never celebrate a decreasing training loss or a flashy demo. Maintain a held-out evaluation suite and test slices.
9. **Treat Tool Output & RAG as Untrusted:** Retrieved documents and web search results are untrusted input vectors for indirect prompt injection. Enforce permission boundaries in deterministic application code, not in the prompt.
10. **Measure Retrieval and Generation Separately:** When a RAG system answers incorrectly, diagnose whether retrieval missed the document, retrieval returned noise, or the model ignored the context.
11. **Inject Failures Intentionally:** You do not understand an AI system until you have broken it, observed its signature, and debugged it.

---

## 3. The 11-Stage Investigative Learning Loop

Every phase in this curriculum executes the following loop:

```text
       ┌──────────┐
       │ Problem  │ (What real-world failure or bottleneck occurs?)
       └────┬─────┘
            ▼
       ┌──────────┐
       │ Predict  │ (Formulate testable hypothesis on memory/latency/behavior)
       └────┬─────┘
            ▼
    ┌───────────────┐
    │Build Primitive│ (Construct raw mechanism with zero high-level abstractions)
    └────┬──────────┘
            ▼
       ┌──────────┐
       │   Run    │ (Execute on local hardware: Tier 1 CPU or Tier 2 GPU)
       └────┬─────┘
            ▼
       ┌──────────┐
       │ Inspect  │ (Examine IR, memory addresses, gradients, or traces)
       └────┬─────┘
            ▼
       ┌──────────┐
       │ Evaluate │ (Verify deterministic and semantic correctness)
       └────┬─────┘
            ▼
       ┌──────────┐
       │ Measure  │ (Profile latency, throughput, TTFT, and memory)
       └────┬─────┘
            ▼
       ┌──────────┐
       │  Break   │ (Inject realistic failure: OOM, graph break, injection)
       └────┬─────┘
            ▼
       ┌──────────┐
       │  Debug   │ (Isolate responsible layer using telemetry and logs)
       └────┬─────┘
            ▼
       ┌──────────┐
       │ Optimize │ (Fuse, tile, quantize, cache, or bound concurrency)
       └────┬─────┘
            ▼
     ┌──────────────┐
     │ Re-evaluate  │ (Verify quality did NOT regress while optimizing)
     └──────────────┘
```

---

## 4. The 10 Completion Rules

A lesson or project is **NOT** complete simply because:
- The script exited with code 0.
- The agent printed an answer.
- The fine-tuning loss decreased.
- A benchmark showed a speedup.

To declare a phase complete, the learner must be able to articulate:
1. **What happened:** Exact chronological sequence of events across software and hardware.
2. **Why it happened:** Physical and computational causality (e.g., memory bandwidth saturation, uncoalesced memory access, graph break).
3. **What was measured:** Metric definitions, instrumentation technique, and units.
4. **What changed:** Concrete delta between baseline and modified implementation.
5. **Which guarantees exist:** Formal guarantees provided by the system (e.g., schema validity, idempotency, mathematical equivalence).
6. **Which guarantees do NOT exist:** Probabilistic risks, edge-case failure modes, and hardware dependencies.
7. **How failure was detected:** What monitor, trace, test, or log exposed the flaw.
8. **How correctness was evaluated:** Ground-truth baseline and evaluation methodology.
9. **What tradeoff was introduced:** Latency vs memory, throughput vs TTFT, precision vs speed, complexity vs maintainability.
10. **Whether the extra complexity was justified:** Would a simpler architecture (e.g., standard code vs agent, retrieval vs fine-tuning) have achieved equal or superior results?

---

## 5. The Standard Evidence Template

Every completed exercise or experiment must fill out this template:

```text
Lesson:
Date:
Python version:
Framework/runtime versions:
Hardware:
GPU if any:
Problem:
Prediction:
Model:
Dataset:
Input shape:
Dtype:
Commands:
Baseline:
Change made:
Measurements:
Evaluation result:
Expected behavior:
Actual behavior:
What did I intentionally break?
Failure observed:
How did I diagnose it?
What layer was responsible?
How did I fix it?
What tradeoff did the fix introduce?
Cost implication:
Security implication:
Artifact produced:
Explain the mechanism in my own words:
Remaining questions:
```
