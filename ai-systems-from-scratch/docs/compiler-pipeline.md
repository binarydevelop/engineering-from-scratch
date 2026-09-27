# The AI Compiler Pipeline: From Python to Machine Instructions

> **Motto:** Code is data. A computation graph is a program waiting to be analyzed, pruned, fused, and lowered.

---

## 1. The End-to-End Compiler Pipeline

In eager mode, PyTorch dispatches operations one by one through the Python C-API. This incurs Python interpreter overhead, launch latencies for every kernel, and forces intermediate tensors into DRAM.

An AI compiler captures the global dataflow and transforms it through multiple abstraction levels:

```text
    ┌───────────────────────────────┐
    │     Python Model Definition   │
    │  y = torch.relu(x @ w + b)   │
    └───────────────┬───────────────┘
                    │
                    ▼ [Graph Capture / Tracing: TorchDynamo / FX]
    ┌───────────────────────────────┐
    │ High-Level Computation Graph  │
    │ Nodes: Matmul, Add, Relu      │
    └───────────────┬───────────────┘
                    │
                    ▼ [Target-Independent Passes: Constant Folding, CSE]
    ┌───────────────────────────────┐
    │  Optimized High-Level IR      │
    │ Pruned dead ops, folded consts│
    └───────────────┬───────────────┘
                    │
                    ▼ [Operator Fusion Pass: Horizontal & Vertical Fusion]
    ┌───────────────────────────────┐
    │       Fused Intermediate IR   │
    │ Single Node: FusedMatmulBiasRelu
    └───────────────┬───────────────┘
                    │
                    ▼ [Lowering / Loop Scheduling: TorchInductor / MLIR]
    ┌───────────────────────────────┐
    │   Structured Loop / Buffer IR │
    │ Nested loops, tiled iterations│
    └───────────────┬───────────────┘
                    │
                    ▼ [Target Codegen: C++ OpenMP / Triton / NVCC]
    ┌───────────────────────────────┐
    │  Generated Machine Kernels    │
    │ SIMD vector ops or GPU kernels│
    └───────────────┬───────────────┘
                    │
                    ▼ [Runtime Execution]
         Hardware Execution (CPU / GPU)
```

---

## 2. The 5 Compiler Optimization Questions

Whenever you apply or observe a compiler optimization, you must answer these five questions:

```text
1. WHAT WORK DISAPPEARED?
   Did we eliminate redundant arithmetic? (e.g., constant folding x * 0 = 0, CSE merging duplicate subgraphs).

2. WHAT MEMORY MOVEMENT DISAPPEARED?
   Did we eliminate intermediate roundtrips to GPU DRAM / CPU cache?
   In eager Add + ReLU, the sum is written to DRAM, then read back by ReLU.
   In fused Add+ReLU, the sum stays in registers!

3. WHAT KERNEL LAUNCHES DISAPPEARED?
   Every kernel launch on a modern GPU takes ~3–10 microseconds of CPU-driver overhead.
   Fusing 5 operations into 1 reduces 5 kernel launches to 1 launch.

4. WHAT SPECIALIZATION WAS ASSUMED?
   Did the compiler assume fixed tensor shapes, fixed strides, or specific dtypes?
   If dynamic shapes vary later, will a guard fail and trigger recompilation?

5. WHAT NEW COMPILATION COST APPEARED?
   Compilation is not free. Ahead-of-time or Just-in-Time (JIT) tracing and kernel code generation takes seconds or minutes.
   Is the compilation overhead amortized across enough steady-state inference runs?
```

---

## 3. High-Level Graph vs Low-Level Kernel IR

| Layer | Representation | Questions Answered | Example Transformations |
| :--- | :--- | :--- | :--- |
| **Graph IR** | Nodes = High-level ops (`conv2d`, `matmul`, `softmax`), Edges = Tensors | What functions are computed? What are the dependencies? | Dead-code elimination, algebraic rewriting, operator fusion. |
| **Loop / Kernel IR** | Nested loops over tensor coordinates, load/store pointers | How are loop iterations mapped to threads, blocks, and memory banks? | Loop tiling, unrolling, vectorization, shared memory caching. |

---

## 4. Multi-Level Intermediate Representation (MLIR)

MLIR solves compiler fragmentation by organizing representations into modular **Dialects**:
- **Tensor Dialect:** High-level value-semantic tensor operations (unranked, dynamic).
- **Linalg Dialect:** Structured operations on multi-dimensional buffers and iteration domains.
- **Affine Dialect:** Polyhedral loop nests with affine memory accesses, enabling formal loop transformations.
- **Arith / Math Dialect:** Primitive scalar arithmetic operations.
- **LLVM / NVVM Dialect:** Low-level machine abstractions ready for machine code assembly.
