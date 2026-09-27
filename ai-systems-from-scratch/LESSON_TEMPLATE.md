# Lesson Template

Use this standardized template when creating any phase or lesson in this repository. Every lesson follows our 15-stage investigative learning cycle.

---

# [Phase NN — Lesson Title]

## Motto
> *[One sentence summarizing the first-principles law or mental model taught by this lesson]*

---

## Problem
*What specific failure, bottleneck, or limitation occurs without this layer? Describe a concrete production scenario where ignorance of this concept leads to failure.*

---

## Prediction
*Before running any code or inspecting logs, write down your hypothesis:*
- What do you predict will happen to latency / memory / accuracy?
- What tensor shapes or memory footprints do you expect?

---

## Why this matters
*How does this fit into the end-to-end chain connecting hardware, compilers, models, and production agent loops?*

---

## First principles
*The mathematical, physical, or logical foundations. No framework code yet.*
- Computational complexity ($O(N)$, $O(N^2)$, FLOP counts)
- Memory bandwidth vs Compute bounds (Arithmetic Intensity)
- Theoretical limits

---

## Mental model
*Visual or structural model. Use ASCII diagrams or flowcharts.*

```text
[Input] ──► [Component A] ──► [Component B] ──► [Output]
```

---

## Build the primitive
*Step-by-step implementation from scratch using raw Python/NumPy or bare PyTorch tensors. Zero high-level abstractions.*

```python
# Raw primitive implementation
```

---

## Use the real tool
*Now that the underlying mechanism is understood, introduce the modern production library or compiler hook (`torch.compile`, `peft`, `vllm`, `pydantic`).*

```python
# Production tool equivalent
```

---

## Inspect it
*Look under the hood. Inspect IR nodes, bytecode, compiled graph, gradient tensors, or raw memory allocations.*

---

## Evaluate it
*Verify correctness against ground truth or baseline. Calculate deterministic error or evaluation metrics.*

---

## Measure it
*Benchmark quantitatively. Record latency (median, p95), memory footprint, or token throughput. Never use single-run measurements.*

---

## Break it
*Deliberately inject a realistic failure mode (e.g., shape mismatch, graph break, numerical underflow, prompt injection, duplicate side effect).*

---

## Debug it
*Locate the faulty layer using profiling, logging, or debugging harnesses. Explain the diagnostic signature.*

---

## Optimize it
*Apply an optimization pass (fusion, tiling, low-rank factorization, caching, rate limiting) and measure the delta.*

---

## Security considerations
*Threat modeling: How could an attacker exploit this layer? Authorization, untrusted input boundaries, data isolation.*

---

## Cost considerations
*Compute, memory, and dollar implications. How does scaling this layer affect request unit economics?*

---

## Evidence
*Record your experimental findings using the standardized Evidence Template:*

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

---

## Questions for mastery
1. *[Conceptual & Architectural tradeoff question]*
2. *[Debugging & Failure analysis question]*
3. *[Quantitative / Capacity planning question]*

---

## When to use this
*Under what explicit production constraints is this technique appropriate?*

---

## When not to use this
*When is this technique over-engineering, harmful, or premature?*

---

## What comes next
*How does this lesson connect directly to the next phase?*
