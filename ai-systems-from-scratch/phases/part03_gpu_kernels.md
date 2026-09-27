# Part III — GPU Kernels & Hardware Modeling (Phases 37 – 50)

> **Motto:** A fast wrong kernel is still wrong. Hardware performance requires matching algorithm access patterns to physical memory hierarchies.

---

## Phases 37 – 42: GPU Execution Model & Memory Hierarchy
- **Phase 37 — GPU Execution Model:** Host-to-device transfers, grids, thread blocks, warps (32 threads), and SIMT execution.
- **Phase 38 — Kernel Launch Overhead:** Measuring CPU-driver launch latency (~5–10 microseconds per launch) and why fusing small ops is essential.
- **Phase 39 — Memory Hierarchy:** Register file, Shared Memory / SRAM, L2 cache, HBM / DRAM transfer costs.
- **Phase 40 — Coalesced Memory Access:** Ensuring adjacent threads read contiguous DRAM addresses to maximize memory bus transaction efficiency.
- **Phase 41 — Tiling:** Partitioning matrices into sub-blocks fitting into L1/L2 caches (`kernels/cpu_tiled_matmul.py`).
- **Phase 42 — Fused Kernels:** Implementing single-pass Linear + Bias + GELU (`kernels/fused_linear_activation.py`).

---

## Phases 43 – 50: Triton Programming & Numerical Tolerances
- **Phase 43 — Introduce Triton:** The Triton programming paradigm: block-level pointers and automatic memory scheduling.
- **Phase 44 — Triton Vector Addition:** First Triton kernel: program ID, block pointers, mask handling (`kernels/triton_kernels.py`).
- **Phase 45 — Triton Fused Activation:** Fused Linear + GELU eliminating global memory writes.
- **Phase 46 — Triton Softmax:** Numerically stable parallel online softmax kernel.
- **Phase 47 — Triton Matrix Multiplication:** 2D block-tiled GEMM with accumulator loops.
- **Phase 48 — Kernel Correctness:** Verifying custom kernels against PyTorch baselines using strict numerical tolerances (`kernels/numerical_tolerances.py`).
- **Phase 49 — Numerical Error & Stability:** FP16 underflow, BF16 precision loss, catastrophic cancellation.
- **Phase 50 — Kernel Benchmarking:** Rigorous methodology: warmups, device synchronization, median, p95, memory throughput (GB/s) (`kernels/kernel_benchmark.py`).
