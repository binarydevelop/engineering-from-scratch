# Part IV — Inference Optimization & Serving (Phases 51 – 70)

> **Motto:** Serving is not just calling `.forward()`. Serving is scheduling memory, batching heterogeneous requests, and managing KV cache churn under concurrent load.

---

## Phases 51 – 58: Scheduling & KV Cache Management
- **Phase 51 — Inference Performance Model:** Dissecting TTFT (Time To First Token), ITL (Inter-Token Latency), and tokens/sec.
- **Phase 52 — Batch Inference:** Amortizing model weight memory loads across multiple concurrent requests.
- **Phase 53 — Static Batching Problem:** The padding bubble problem: stragglers stall the entire batch.
- **Phase 54 — Continuous Batching Simulator:** Iteration-level dynamic scheduling (`inference/continuous_batching_scheduler.py`).
- **Phase 55 — KV Cache Memory Accounting:** Exact memory calculation across layers, heads, and context lengths (`inference/kv_cache.py`).
- **Phase 56 — KV Cache Fragmentation:** Internal and external memory fragmentation in contiguous buffer allocation.
- **Phase 57 — Paged KV Cache:** Virtual memory-style block allocation eliminating external fragmentation (`inference/paged_kv_cache.py`).
- **Phase 58 — Prefix Caching:** Hash-indexed caching of repeated system prompt tokens (`inference/prefix_caching.py`).

---

## Phases 59 – 65: Quantization & Speculative Decoding
- **Phase 59 — Quantization Motivation:** Memory bandwidth wall: calculating memory requirements for 7B/70B models.
- **Phase 60 — Quantization From First Principles:** Scale and zero-point mapping, quantize/dequantize (`inference/quantization_engine.py`).
- **Phase 61 — Weight-Only Quantization:** Symmetric INT8 weight-only linear layer simulation.
- **Phase 62 — INT8 vs INT4 Concepts:** Groupwise scaling, sub-byte packing, activation outlier challenges.
- **Phase 63 — Calibration:** Post-Training Quantization (PTQ) activation calibration over representative datasets.
- **Phase 64 — Quantization Error Evaluation:** Evaluating perplexity and downstream task accuracy regressions after quantization.
- **Phase 65 — Speculative Decoding:** Draft model proposes $K$ tokens; target model verifies concurrently (`inference/speculative_decoding.py`).

---

## Phases 66 – 70: Parallelism & Production Serving Engines
- **Phase 66 — Tensor Parallelism:** Row and Column linear sharding with All-Reduce communications.
- **Phase 67 — Pipeline Parallelism:** Layer partitioning across GPUs, 1F1B scheduling, pipeline bubbles.
- **Phase 68 — Data Parallel Inference:** Independent model replicas with load balancing across GPU workers.
- **Phase 69 — Introduce vLLM Engine:** Mapping manual schedulers, paging, and caches to modern production vLLM.
- **Phase 70 — Serving Benchmark:** Load-testing serving engines: measuring TTFT, throughput, and p99 under concurrent load.
