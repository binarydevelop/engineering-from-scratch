# Part I — Model Execution Foundations (Phases 00 – 11)

> **Motto:** Before you compile a model or serve a token, you must be able to trace numbers through memory.

---

## Phase 00 — AI Systems Laboratory
- **Problem:** Unreproducible environments, mismatched library ABIs, and opaque GPU hardware allocations cause silent performance and correctness failures.
- **First Principles:** Every system layer (OS kernel, libc, Python runtime, PyTorch C++ bindings, CUDA runtime, and GPU microarchitecture) must be explicitly queried and verified.
- **Mental Model:**
  ```text
  Hardware Accelerator (CUDA/MPS/CPU) ◄── Device Driver ◄── PyTorch C++ Core ◄── Python Binding
  ```
- **Build the Primitive:** Run `scripts/check-environment.sh` and `scripts/check-gpu.py` to inspect platform, PyTorch build flags, and memory.
- **Measure:** Measure device allocation latency and inspect memory headroom.
- **Break:** Attempt to allocate a 50GB tensor on a device with 8GB memory; observe CUDA/system OOM signature.

---

## Phase 01 — From Model Code to Numbers
- **Problem:** Learners treat neural networks as mystical black boxes rather than nested linear algebra transformations.
- **First Principles:** A 2-layer MLP is strictly: $h = \text{ReLU}(X W_1 + b_1)$, $Y = h W_2 + b_2$.
- **Mental Model:**
  ```text
  Input [B, D_in] ──► Matmul [D_in, D_h] ──► Add Bias [D_h] ──► ReLU ──► Matmul [D_h, D_out]
  ```
- **Build the Primitive:** Write a handcrafted MLP using pure nested Python lists or bare NumPy arrays.
- **Measure:** Print shapes and memory layout at every intermediate step.

---

## Phase 02 — Tensor Shape Reasoning
- **Problem:** Shape mismatch errors (`RuntimeError: matmul dimension mismatch`) account for over 50% of deep learning runtime bugs.
- **First Principles:** Contraction dimension $K$ in $[M, K] \times [K, N] \to [M, N]$ must match identically. Batch dimensions must follow NumPy broadcasting rules.
- **Mastery Question:** Given tensor $A \in \mathbb{R}^{B \times 1 \times S \times D}$ and $B \in \mathbb{R}^{1 \times H \times D \times D}$, what is the exact output shape and how many scalar floating-point values are generated?

---

## Phase 03 — Dtypes & Precision
- **Problem:** Blindly casting tensors to lower precision causes numerical overflow or loss of gradient signal.
- **First Principles:**
  - **FP32:** 1 sign, 8 exponent, 23 mantissa (Range $\pm 3.4 \times 10^{38}$, $\epsilon \approx 1.19 \times 10^{-7}$).
  - **FP16:** 1 sign, 5 exponent, 10 mantissa (Range $\pm 65,504$ — easily overflows!).
  - **BF16:** 1 sign, 8 exponent, 7 mantissa (Preserves FP32 dynamic range, but lower precision).
- **Inspect:** Run `kernels/numerical_tolerances.py` to observe precision loss and machine epsilon.

---

## Phase 04 — Tensor Memory Layout & Strides
- **Problem:** Transposing a tensor changes its view but not its underlying physical memory buffer, causing non-contiguous memory access penalties.
- **First Principles:** Stride vector $[s_0, s_1]$ indicates how many physical memory elements to jump to advance by 1 along dimension $d$. In row-major, $s_1 = 1, s_0 = \text{cols}$.
- **Break:** Call `.view(-1)` on a transposed tensor without calling `.contiguous()`; observe `RuntimeError: view size is not compatible with input tensor's size and stride`.

---

## Phase 05 — Matrix Multiplication Cost
- **Problem:** Inability to estimate whether a matrix multiplication will take 1ms or 1 hour.
- **First Principles:** Multiplying $[M, K]$ by $[K, N]$ requires $M \times N$ dot products, each taking $K$ multiplications and $K$ additions:
  $$\text{FLOPs} = 2 \times M \times N \times K$$
- **Measure:** Calculate theoretical TFLOPs achieved using `scripts/benchmark.py`.

---

## Phase 06 — Memory vs Compute Bounds (The Roofline Model)
- **Problem:** Optimizing arithmetic code when the operation is completely throttled by memory bus bandwidth.
- **First Principles:**
  $$\text{Arithmetic Intensity} = \frac{\text{Floating Point Operations (FLOPs)}}{\text{DRAM Bytes Transferred}}$$
- **Rule:** If $\text{Intensity} < \frac{\text{Peak Compute (TFLOPs)}}{\text{Memory Bandwidth (TB/s)}}$, the operation is **Memory-Bound**.

---

## Phase 07 — Transformer Inference Trace
- **Problem:** Framework abstractions hide the chronological execution path of multi-head self-attention.
- **First Principles:** Trace step-by-step:
  ```text
  Token IDs [B, S] ──► Token Embeddings + Positional Encoding [B, S, D]
    ──► Linear Q, K, V Projections [B, S, D]
    ──► Split into H Heads [B, H, S, d_k]
    ──► Scaled Dot-Product Attention: Softmax(Q K^T / sqrt(d_k)) V
    ──► Concat Heads & Out Projection [B, S, D]
    ──► MLP / Feed-Forward Block: Linear -> GELU -> Linear [B, S, D]
    ──► LayerNorm & Unembed -> Logits [B, S, Vocab]
  ```

---

## Phase 08 — Attention From First Principles
- **Problem:** Memory allocation explodes quadratically with prompt length during self-attention.
- **First Principles:** The intermediate attention matrix $QK^T$ has shape $[B, H, S, S]$. Memory scales as $O(S^2)$.
- **Measure:** Measure peak tensor bytes as sequence length increases from 512 to 8,192 tokens.

---

## Phase 09 — Autoregressive Generation
- **Problem:** Naive autoregressive generation feeds the entire accumulated token history $[x_1, \dots, x_t]$ into the model at every step, recomputing past activations repeatedly.
- **Evidence:** Generation of $N$ tokens without caching costs $O(N^3)$ total operations.

---

## Phase 10 — KV Cache Motivation
- **Problem:** Eliminating redundant prompt and historical token recomputations.
- **First Principles:** Since previous tokens do not change during autoregressive decoding, their Key and Value vectors are identical across steps. Caching them reduces generation step complexity from $O(S^2)$ to $O(S)$.
- **Build the Primitive:** Inspect `inference/kv_cache.py`.

---

## Phase 11 — Prefill vs Decode
- **Problem:** Treating all LLM token computations as having equal performance characteristics.
- **First Principles:**
  - **Prefill:** Computes embeddings for all prompt tokens in parallel. Large GEMM ($[B, S, D] \times [D, D]$). Highly parallel, compute-bound.
  - **Decode:** Emits one token at a time. Matrix-vector product ($[B, 1, D] \times [D, D]$). Memory bandwidth-bound.
- **Serving Implication:** Prefill governs **TTFT**; Decode governs **Inter-Token Latency (ITL)**.
