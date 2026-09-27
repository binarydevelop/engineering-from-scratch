# The AI Inference Runtime & Serving Architecture

> **Motto:** Serving is not just calling `.forward()`. Serving is scheduling memory, batching heterogeneous requests, and managing KV cache churn under concurrent load.

---

## 1. The Serving Request Lifecycle

```text
       [ User Request: "Translate the following..." ]
                          │
                          ▼
                 ┌──────────────────┐
                 │    Tokenizer     │ ──► [Token IDs: [15496, 262, ...]]
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │  Request Queue   │ ──► (Pending requests waiting for GPU allocation)
                 └────────┬─────────┘
                          │
                          ▼
           ┌──────────────────────────────┐
           │ Dynamic Continuous Scheduler │ ◄── [Checks Available KV Cache Blocks]
           └──────────────┬───────────────┘
                          │
        ┌─────────────────┴─────────────────┐
        ▼                                   ▼
┌───────────────────────────────┐ ┌───────────────────────────────┐
│     Prefill Phase (Batch)     │ │     Decode Phase (Batch)      │
│ Compute prompt representations│ │ Generate 1 token per request  │
│ High Arithmetic Intensity     │ │ Memory Bandwidth Bound        │
│ Compute Bound ($O(S^2)$)      │ │ Memory Bound ($O(S)$ per tok) │
└───────────────┬───────────────┘ └───────────────┬───────────────┘
                │                                 │
                ▼                                 ▼
        ┌─────────────────────────────────────────────────┐
        │        Paged KV Cache Memory Manager            │
        │ Allocates non-contiguous physical memory blocks │
        │ Prevents memory fragmentation                   │
        └───────────────────────┬─────────────────────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │    Sampling Layer     │
                    │ Temperature, Top-p,   │
                    │ Greedy, Logit masking │
                    └───────────┬───────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │     Detokenizer       │ ──► [Streaming SSE / Chunked HTTP]
                    └───────────┬───────────┘
                                │
                                ▼
                    [ Client HTTP Response ]
```

---

## 2. The 4 Distinct Serving Metrics

In traditional web backends, we measure simple request latency ($t_{\text{end}} - t_{\text{start}}$).  
In LLM serving, single latency numbers obscure fundamental system bottlenecks. You MUST track four distinct metrics:

### 1. TTFT (Time To First Token)
- **Definition:** The time elapsed from when the request enters the server until the very first generated token is emitted to the client.
- **Governed by:** Queue wait time + **Prefill phase latency**.
- **User impact:** Perceived responsiveness. If TTFT is slow, the user feels the system is lagging.

### 2. ITL (Inter-Token Latency) / TPOT (Time Per Output Token)
- **Definition:** The time between each subsequent token emitted during autoregressive decoding.
- **Governed by:** **Decode phase execution time** (heavily memory bandwidth-bound, governed by GPU memory clock and KV cache read speed).
- **User impact:** Reading fluidity. Humans read comfortably at ~15–25 tokens/second (40–65 ms ITL).

### 3. End-to-End Request Latency (E2E Latency)
- **Definition:** Total time for the full generation:
  $$\text{E2E Latency} = \text{TTFT} + (N_{\text{output}} - 1) \times \text{ITL}$$
- **Governed by:** Combined prefill latency and cumulative decode loop duration.

### 4. System Throughput (Tokens/Second & Requests/Second)
- **Definition:** Aggregate generation rate across all concurrent streams:
  $$\text{Throughput} = \frac{\sum \text{Generated Tokens}}{\text{Total Elapsed Seconds}}$$
- **Governed by:** Continuous batching efficiency, GPU compute saturation, and memory fragmentation prevention (PagedAttention).

---

## 3. Prefill vs Decode: The Fundamental Split

| Dimension | Prefill Phase | Decode Phase |
| :--- | :--- | :--- |
| **Input Shape** | $[B, S_{\text{prompt}}, D]$ (Matrix-Matrix GEMM) | $[B, 1, D]$ (Matrix-Vector GEMV) |
| **Operational Bound** | **Compute-Bound** (High arithmetic intensity) | **Memory-Bound** (Low arithmetic intensity) |
| **KV Cache Role** | Populates new keys and values for prompt | Reads full historical KV cache, appends 1 new entry |
| **Parallelism** | Parallel across all prompt tokens | Strictly sequential token-by-token loop |
| **Optimization Strategy** | Tensor parallelism, FlashAttention tiling | PagedAttention, KV-cache quantization, speculative decoding |

---

## 4. Why Continuous Batching is Mandatory

In naive **Static Batching**, requests $[R_1, R_2, R_3]$ are padded to the longest request length. If $R_1$ needs 10 output tokens and $R_2$ needs 500 output tokens:
- $R_1$ finishes in 10 steps but sits idle, occupying GPU VRAM while waiting for $R_2$ to finish 500 steps.
- The GPU performs dummy computations on padding tokens.

In **Continuous Batching (Iteration-Level Scheduling)**:
- As soon as $R_1$ emits an EOS (End of Sequence) token, it is evicted immediately.
- A new request $R_4$ enters the batch at the very next decode iteration.
- Zero wasted padding computation; GPU utilization approaches theoretical maximum.
