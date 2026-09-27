# Part II — Compilers From First Principles (Phases 12 – 36)

> **Motto:** Code is data. A computation graph is a program waiting to be analyzed, pruned, fused, and lowered.

---

## Phases 12 – 17: Graphs, Optimization & Fusion
- **Phase 12 — Why AI Compilers Exist:** Overhead of eager Python dispatch, temporary memory traffic, and kernel launch tax.
- **Phase 13 — Computation Graphs:** Representing operations as Directed Acyclic Graphs (DAGs). Nodes = Ops, Edges = Tensors.
- **Phase 14 — Graph Execution (`mini_graph_runtime.py`):** Topological interpreter evaluating graph nodes.
- **Phase 15 — Graph Optimization:** Constant folding ($2 + 3 \to 5$) and dead node elimination.
- **Phase 16 — Common Subexpression Elimination (CSE):** Detecting and merging duplicate subtrees.
- **Phase 17 — Operator Fusion:** Fusing Add + ReLU into a single loop, eliminating DRAM roundtrips.
- **Hands-on Lab:** Inspect and execute `compiler-labs/mini_graph_runtime.py` and `compiler-labs/operator_fusion.py`.

---

## Phases 18 – 25: Intermediate Representation (IR), SSA & Shapes
- **Phase 18 — Intermediate Representation (IR):** Textual representations bridging high-level Python and low-level machine code.
- **Phase 19 — SSA Intuition:** Static Single Assignment (`%0 = ...`, `%1 = ...`), immutability, and dependency analysis.
- **Phase 20 — Compiler Passes:** Pass manager executing sequential transformation passes.
- **Phase 21 — Pattern Rewriting:** Algebraic identities (`x * 1 -> x`, `x + 0 -> x`).
- **Phase 22 — Canonicalization:** Normalizing algebraically equivalent syntax before optimization.
- **Phase 23 — Shape Propagation:** Inferring output tensor shapes symbolically through graphs (`compiler-labs/shape_propagation.py`).
- **Phase 24 — Static vs Dynamic Shapes:** Specialization tradeoffs: polymorphic dynamic kernels vs peak static performance.
- **Phase 25 — Graph Breaks:** Python dynamic behavior breaking graph capture: data-dependent control flow.

---

## Phases 26 – 30: TorchDynamo & TorchInductor
- **Phase 26 — Introduce `torch.compile`:** Comparing eager execution against TorchDynamo + TorchInductor.
- **Phase 27 — TorchDynamo Mental Model:** Bytecode interception, frame evaluation, guards, and FX graph capture.
- **Phase 28 — Guards & Recompilation:** Triggering guard failures via shape variations and inspecting recompilation overhead.
- **Phase 29 — Compiler Backend:** Distinguishing graph frontends from hardware codegen backends.
- **Phase 30 — TorchInductor:** Inspecting Inductor generated C++ OpenMP and Triton code.
- **Hands-on Lab:** Inspect and execute `compiler-labs/torch_compile_inspection.py`.

---

## Phases 31 – 36: Multi-Level Intermediate Representation (MLIR)
- **Phase 31 — MLIR Motivation:** Overcoming compiler fragmentation via multi-level dialects.
- **Phase 32 — MLIR Dialects:** Abstraction hierarchy: Tensor $\to$ Linalg $\to$ Affine $\to$ LLVM dialects.
- **Phase 33 — MLIR Operations:** Anatomy of an op: operands, results, regions, attributes, and types.
- **Phase 34 — MLIR Passes & Rewriting:** Dialect conversion infrastructure.
- **Phase 35 — Lowering:** Progressively translating declarative tensor operations into structured loop nests.
- **Phase 36 — Hardware-Aware Compilation:** Specializing execution strategies for CPU SIMD vs GPU SIMT cores.
- **Hands-on Lab:** Inspect and execute `compiler-labs/mlir_toy_dialect.py`.
