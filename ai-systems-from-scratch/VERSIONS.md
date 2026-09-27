# Version Discipline & Environment Matrix

**Repository Generation Date:** 2026-09-25  
**Course Version:** 1.0.0-LTS  
**Repository Motto:** *Understand it. Build it. Train it. Compile it. Serve it. Evaluate it. Break it. Debug it. Optimize it. Operate it.*

---

## 1. Verified Software & Library Stack

This repository pins and verifies modern stable interfaces across the Python, PyTorch, compilation, serving, and agent ecosystem.

| Component / Library | Pinned / Tested Version | Role / Scope in Repository | Interface Status |
| :--- | :--- | :--- | :--- |
| **Python** | `3.12.x` (>=3.10 supported) | Base runtime for all implementations | Stable Standard |
| **PyTorch** | `2.14.0` (>=2.2.0) | Core tensor runtime, Autograd, TorchDynamo, TorchInductor | Public Stable API |
| **CUDA Toolkit** | `12.4` / `12.6` (Tier 2/3) | GPU runtime, driver, NVCC compiler toolchain | Hardware Dependent |
| **Triton** | `3.0.x` / `2.3.x` | Domain-specific GPU programming language for fused kernels | Public Stable API (Linux/CUDA) |
| **Transformers** | `5.17.0` (>=4.40.0) | Model architectures, tokenizers, generation configs | Public Stable API |
| **PEFT** | `0.21.0` (>=0.10.0) | LoRA, QLoRA, adapter injection & merging | Public Stable API |
| **TRL** | `1.13.0` (>=0.8.0) | SFTTrainer, DPOTrainer, preference optimization | Public Stable API |
| **Accelerate** | `1.15.0` (>=0.30.0) | Distributed device placement, mixed-precision dispatch | Public Stable API |
| **vLLM** | `0.6.x` / `0.5.x` | PagedAttention, continuous batching inference serving engine | Production Engine (Linux/CUDA) |
| **Pydantic** | `2.13.5` (>=2.5.0) | Tool schema validation, structured JSON output validation | Public Stable API |
| **Pytest** | `9.1.1` (>=8.0.0) | Automated testing, correctness, regression suites | Developer Tool |

---

## 2. Abstraction Classification Guide

To prevent learners from conflating timeless math with ephemeral library syntax, every concept in this repository is strictly tagged with one of four classifications:

### A. Mathematical Concept (Timeless)
- **Examples:** Matrix multiplication FLOPs ($2MNK$), Attention mechanism ($\text{softmax}(QK^T / \sqrt{d_k})V$), Cross-Entropy loss ($-\sum y_i \log \hat{y}_i$), Low-Rank update decomposition ($\Delta W = A \cdot B$), Bradley-Terry preference probability ($P(y_w \succ y_l \mid x) = \sigma(r(x, y_w) - r(x, y_l))$).
- **Longevity:** Decades. Independent of programming languages or frameworks.

### B. Research Technique (Methodological)
- **Examples:** Low-Rank Adaptation (LoRA), Quantized Low-Rank Adaptation (QLoRA), Direct Preference Optimization (DPO), Speculative Decoding, PagedAttention, FlashAttention tiling.
- **Longevity:** 3–10 years. May be superseded by newer algorithmic architectures, but foundational to modern systems.

### C. Public Framework API (Standard Contract)
- **Examples:** `torch.compile(model, backend="inductor")`, `peft.LoraConfig`, `trl.DPOTrainer`, `vllm.LLM(model=...)`.
- **Longevity:** 1–3 years. Subject to framework deprecation cycles and migration guides.

### D. Implementation Detail / Private Internals (Volatile)
- **Examples:** TorchDynamo bytecode transformation hooks, TorchInductor private lowering tables, Triton temporary JIT directories, CUDA warp-scheduler dispatch slots.
- **Longevity:** Months. Never treat internal flags as public contracts!

---

## 3. Deprecated vs Modern Interface Policy

| Legacy / Deprecated Pattern | Modern Standard (Used Here) | Why Deprecated / Replaced |
| :--- | :--- | :--- |
| `torch.jit.trace` / `torch.jit.script` | `torch.compile` (Dynamo + Inductor) | TorchScript required awkward C++ type annotations and struggled with dynamic control flow. Dynamo captures PyTorch frame graphs cleanly. |
| `bitsandbytes` hardcoded linear overrides | Official `peft` quantization hooks / NF4 dispatch | Clean adapter abstraction, interoperable checkpoint serialization. |
| Custom regex JSON extractors | Structured outputs (`Pydantic` schema enforcement + JSON Grammar masking) | Regex parsing fails on escape sequences and nested tool parameters. |
| Prompt-engineered "agents" in single loop | Explicit Finite State Machine / Router / Tool Loop | Unconstrained prompt loops burn budget and enter infinite loops under production load. |
| `OpenAI Completion` raw endpoints | OpenAI Chat Completions / Tool-Calling schema API | Completion API lacked first-class tool calling, role typing, and structured outputs. |

---

## 4. Hardware Tiers & Platform Notes

### Tier 1: CPU / Universal
- Compatible with all operating systems (macOS Apple Silicon, Linux x86_64, Windows WSL2).
- Supported: All 231 phases conceptually, mini compiler graph IRs, CPU tiled matmul, manual training loop, manual agent loop, RAG, and eval harnesses.

### Tier 2: Single Consumer GPU (NVIDIA CUDA 8GB–24GB VRAM)
- Linux / WSL2 recommended for Triton and vLLM.
- Supported: Triton GPU kernel authoring, local SFT/LoRA fine-tuning, 4-bit quantization, and vLLM inference server.

### Tier 3: Multi-GPU / Cloud Optional (2+ GPUs)
- Tensor parallelism, pipeline parallelism, distributed data parallel training.
- Simulation equivalents provided for Tier 1 users.
