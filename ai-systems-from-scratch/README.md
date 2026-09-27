# AI Systems From Scratch

> **Understand it. Build it. Train it. Compile it. Serve it. Evaluate it. Break it. Debug it. Optimize it. Operate it.**

---

```text
                  THIS IS NOT A PROMPT-ENGINEERING REPOSITORY.
                  THIS IS A COURSE IN AI SYSTEMS ENGINEERING.
```

**AI Systems Engineering is the discipline of adapting, optimizing, serving, orchestrating, evaluating, securing, and operating probabilistic models inside reliable software systems.**

The learner should NOT think:
```text
AI Engineering = call model API + prompt + vector database
```

Instead, you will trace, build, and optimize the complete stack:

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

and for model adaptation:

```text
dataset
  ↓
tokenization
  ↓
training examples
  ↓
forward pass
  ↓
loss calculation
  ↓
backpropagation
  ↓
optimizer step
  ↓
parameter update / LoRA adapter
  ↓
evaluation & checkpointing
  ↓
model serving runtime
```

---

## The Three Converging Tracks

```text
┌─────────────────────────────────┐
│ Track A: AI Compilers & Kernels │
│ Tensor ops → Graph IR → Fusion  │
│ → Lowering → GPU Kernels → vLLM │
└────────────────┬────────────────┘
                 │
                 │      ┌────────────────────────────────────┐
                 │      │ Track B: Fine-Tuning & Adaptation  │
                 ├─────►│ Training Loop → SFT → LoRA → QLoRA │
                 │      │ → DPO → Alignment → Checkpointing  │
                 │      └─────────────────┬──────────────────┘
                 │                        │
┌────────────────┴────────────────┐       │
│ Track C: Production Agent Sys.  │       │
│ Manual Loop → Schemas → Tools   ├───────┘
│ → State → RAG → Security → Evals│
└────────────────┬────────────────┘
                 │
                 ▼
 ┌───────────────────────────────────────────────┐
 │ CONVERGENCE: FULL PRODUCTION AI SYSTEMS        │
 │ Fine-Tuned Model + Optimized Inference Engine │
 │ + Sandboxed Agent Runtime + Full Observability│
 └───────────────────────────────────────────────┘
```

---

## Critical Teaching Rule: Problem First, Primitive Second, Tool Third

We never start with high-level abstractions:
- **Do not start with `agent = Agent(...)`:** Build the manual `while not done:` loop, JSON deserializer, tool dispatcher, and state machine first.
- **Do not start with `model = torch.compile(model)`:** Trace Python dispatch overhead, write computation graph nodes, implement constant folding and operator fusion passes manually first.
- **Do not start with `LoRA makes fine-tuning cheap`:** Start with dense weight matrix $W$, calculate parameter memory for $\Delta W$, derive $\Delta W \approx A \times B$, and implement low-rank linear layers from raw tensors first.

---

## Hardware Execution Tiers

No learner should be blocked by lacking access to expensive multi-GPU clusters.

| Tier | Minimum Hardware | Target Capabilities |
| :--- | :--- | :--- |
| **Tier 1: CPU / Universal** | Any modern laptop (macOS / Linux / Windows) | All conceptual foundations, tiny transformers, computation graphs, IR passes, CPU tiled GEMM, manual training loops, manual agent loops, evaluations, and security labs. |
| **Tier 2: Single Consumer GPU** | 1x NVIDIA GPU (8GB–24GB VRAM) | Triton GPU kernels, local SFT/LoRA fine-tuning, INT4 quantization, and vLLM single-node serving. |
| **Tier 3: Multi-GPU / Cloud** | 2+ GPUs (Optional advanced labs) | Tensor parallelism (TP), pipeline parallelism, and distributed model serving. *(Simulations provided for Tier 1)* |

---

## Repository Structure

```text
ai-systems-from-scratch/
├── README.md                      # Manifest & philosophy
├── ROADMAP.md                     # Comprehensive 231-phase breakdown
├── LEARNING.md                    # Learning methodology & 10 completion rules
├── LESSON_TEMPLATE.md             # Standardized 15-stage lesson template
├── VERSIONS.md                    # Environment matrix & version discipline
├── COST_SAFETY.md                 # Cloud GPU budgeting & teardown checklist
├── SECURITY.md                    # AI security: injections, sandboxing, auth
├── EVALUATION.md                  # Statistical rigor & evaluation discipline
├── CONTRIBUTING.md                # Development guidelines
├── pyproject.toml                 # Dependencies & build configuration
├── Makefile                       # Unified test & benchmark commands
│
├── scripts/                       # System checks, benchmarks, cleanup
│   ├── check-environment.sh       # Hardware & library detector
│   ├── check-gpu.py               # GPU memory & capability inspector
│   ├── benchmark.py               # Master latency & throughput benchmark
│   └── cleanup.sh                 # Cache & temporary file cleaner
│
├── compiler-labs/                 # Graph IR, passes, SSA, fusion, MLIR dialect
├── kernels/                       # CPU tiled GEMM, Triton kernels, tolerances
├── inference/                     # Continuous batching, PagedAttention, quantization
├── training/                      # Manual loop, autograd, SGD/AdamW, grad accum
├── datasets/                      # Data cleaning, deduplication, packing, templates
├── evaluation/                    # Deterministic, LLM judge, regression suites
├── agents/                        # Framework-free agent loops, state, memory
├── tools/                         # Validated, sandboxed, idempotent tool suite
├── benchmarks/                    # 20+ reproducible performance experiments
├── broken-systems/                # 40+ failure injection labs & solutions
├── experiments/                   # Integration studies (LoRA vs RAG vs Prompt)
├── projects/                      # 15 substantial end-to-end systems
├── capstones/                     # 8 production-grade integration capstones
├── docs/                          # Architecture guides & mental models
└── outputs/                       # Benchmark data, traces, and artifacts
```

---

## Quickstart

### 1. Set Up Environment
```bash
# Clone and enter repository
cd ai-systems-from-scratch

# Create environment and install dependencies
make setup

# Verify your hardware tier and installed runtimes
make check-env
make check-gpu
```

### 2. Run Automated Verification Suite
```bash
make test
```

### 3. Run First Benchmark
```bash
make benchmark
```

---

## The Learning Loop

Every phase in this curriculum executes:

```text
MOTTO ──► PROBLEM ──► PREDICT ──► FIRST PRINCIPLES ──► MENTAL MODEL
  │
  ▼
BUILD PRIMITIVE ──► USE REAL TOOL ──► INSPECT ──► EVALUATE
  │
  ▼
MEASURE ──► BREAK ──► DEBUG ──► OPTIMIZE ──► RE-EVALUATE ──► EVIDENCE
```

---

## Completion Standard

You are finished when a production report of:
```text
"Our AI feature is slow, expensive, and unreliable."
```
does **NOT** make you immediately reach for:
* a larger model
* more prompts
* another agent framework
* vector search by default

Instead, you methodically locate the faulty layer, measure it, test it, and optimize the real bottleneck.
