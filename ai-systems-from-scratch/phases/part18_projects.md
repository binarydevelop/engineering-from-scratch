# Part XVIII — Substantial Projects (Phases 208 – 222)

> **Motto:** Primitives combine into architectures. Build 15 substantial end-to-end systems from the ground up.

---

## The 15 Core Engineering Projects

1. **Phase 208 — Project: Mini Tensor Compiler (`projects/p01_mini_tensor_compiler.py`)**: Computation graph builder, constant folding, dead-node elimination, and topological interpreter runtime.
2. **Phase 209 — Project: Tiny MLIR-Style IR (`compiler-labs/mlir_toy_dialect.py`)**: Multi-level IR with operations, types, dialects, and lowering passes.
3. **Phase 210 — Project: Triton Kernel Pack (`kernels/triton_kernels.py`)**: High-performance vector addition, GELU activation, RMSNorm, and 2D tiled GEMM kernels.
4. **Phase 211 — Project: Mini Inference Scheduler (`projects/p04_mini_inference_scheduler.py`)**: Continuous batching iteration scheduler with priority queue and memory management.
5. **Phase 212 — Project: Quantized Model Experiment (`inference/quantization_engine.py`)**: Comprehensive benchmark comparing FP32, FP16, INT8, and INT4 memory, latency, and perplexity.
6. **Phase 213 — Project: Fine-Tune a Domain Model**: End-to-end domain adaptation pipeline: dataset cleaning, baseline eval, LoRA training, and serving.
7. **Phase 214 — Project: Preference Optimization (DPO)**: Creating preference pairs ($x, y_w, y_l$), training with DPO, and measuring win rate over baseline.
8. **Phase 215 — Project: Evaluation Harness (`projects/p08_evaluation_harness.py`)**: Automated regression evaluation suite with deterministic graders and statistical gating.
9. **Phase 216 — Project: Tool-Using Agent From Scratch (`agents/manual_agent_loop.py`)**: Framework-free autonomous agent with schemas, validation, state, and retries.
10. **Phase 217 — Project: Production RAG System (`projects/p10_production_rag_system.py`)**: Hybrid search (BM25 + vector similarity), chunking, and citation tracking.
11. **Phase 218 — Project: Research Agent**: Multi-turn query decomposition, provenance tracking, and budget circuit breakers.
12. **Phase 219 — Project: Coding Agent Sandbox (`projects/p12_coding_agent_sandbox.py`)**: Sandboxed code execution runtime with resource caps, test runners, and AST validation.
13. **Phase 220 — Project: Customer Support Agent**: Read-only knowledge retrieval, human approval escalation for refunds, policy enforcement.
14. **Phase 221 — Project: Data Analysis Agent**: Safe SQL query generation, SQLite sandbox execution, and chart verification.
15. **Phase 222 — Project: Multi-Agent Workflow**: Deterministic orchestrator coordinating researcher, writer, and editor agents without unconstrained chatter.
