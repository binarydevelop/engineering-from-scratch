# AI Systems Engineering Master Roadmap

> **Motto:** Understand it. Build it. Train it. Compile it. Serve it. Evaluate it. Break it. Debug it. Optimize it. Operate it.  
> **Structure:** 19 Parts | 231 Consecutive Phases | 3 Converging Tracks

---

## The Three Converging Tracks

```text
Track A: AI Compilers & Inference ──┐
Track B: Model Adaptation & PEFT  ──┼──► Convergence: Production AI Systems Engineering
Track C: Production Agent Systems ──┘
```

---

## Summary of Curriculum Parts

| Part | Title | Phase Range | Primary Focus | Hardware Tier |
| :--- | :--- | :--- | :--- | :--- |
| **Part I** | Model Execution Foundations | 00 – 11 | Tensors, shapes, dtypes, memory strides, attention, KV cache | Tier 1 (CPU) |
| **Part II** | Compilers From First Principles | 12 – 36 | Computation graphs, IR, SSA, passes, fusion, `torch.compile`, MLIR | Tier 1 (CPU) |
| **Part III** | GPU Kernels & Hardware Modeling | 37 – 50 | GPU execution model, tiling, Triton kernels, numerical error | Tier 1 / Tier 2 |
| **Part IV** | Inference Optimization & Serving | 51 – 70 | Continuous batching, PagedAttention, quantization, vLLM | Tier 1 / Tier 2 |
| **Part V** | Training From First Principles | 71 – 80 | Autograd, cross-entropy, manual SGD/AdamW, gradient accumulation | Tier 1 (CPU) |
| **Part VI** | Fine-Tuning & Model Adaptation | 81 – 102 | Dataset design, SFT, low-rank factorization, LoRA, QLoRA | Tier 1 / Tier 2 |
| **Part VII** | Preference Optimization | 103 – 111 | Reward modeling, DPO, GRPO, reward hacking & alignment evals | Tier 1 / Tier 2 |
| **Part VIII**| Model Evaluation Rigor | 112 – 120 | Deterministic evals, LLM-as-judge debiasing, regression suites | Tier 1 (CPU) |
| **Part IX** | Agents From First Principles | 121 – 133 | Manual while loop, schemas, tool validation, state, memory | Tier 1 (CPU) |
| **Part X** | Retrieval Systems (RAG) | 134 – 144 | Lexical search, embeddings, similarity, chunking, reranking | Tier 1 (CPU) |
| **Part XI** | Workflows & Orchestration | 145 – 154 | State machines, routers, planner/executor, multi-agent skepticism | Tier 1 (CPU) |
| **Part XII** | Agent Security & Trust Boundaries | 155 – 163 | Prompt injection, tool permissions, sandboxing, secret isolation | Tier 1 (CPU) |
| **Part XIII**| Production Agent Reliability | 164 – 174 | Timeouts, retries, backoff, idempotency tokens, rate limits | Tier 1 (CPU) |
| **Part XIV** | AI Observability & Tracing | 175 – 180 | OpenTelemetry traces, token cost tracking, failure taxonomy | Tier 1 (CPU) |
| **Part XV** | Production Evaluation Gates | 181 – 186 | Offline/online evals, shadow testing, canary releases, gates | Tier 1 (CPU) |
| **Part XVI** | End-to-End System Performance | 187 – 194 | Latency budgeting, prompt economics, adapter serving | Tier 1 / Tier 2 |
| **Part XVII**| Broken AI Systems (40+ Labs) | 195 – 207 | Systematic failure injection, diagnosis & isolated repair | Tier 1 / Tier 2 |
| **Part XVIII**| Substantial Projects (15 Projects)| 208 – 222 | Full compiler, scheduler, kernel pack, RAG, research agent | Tier 1 / Tier 2 |
| **Part XIX** | Capstones & Final Challenge | 223 – 230 | End-to-end platforms, failure day, cost reduction, final enterprise challenge | Tier 1 / Tier 2 / 3 |

---

## Detailed Phase Breakdown

### PART I — MODEL EXECUTION FOUNDATIONS
- **Phase 00 — AI Systems Laboratory:** Reproducible environment, python/torch inspection, device discovery.
- **Phase 01 — From Model Code to Numbers:** Handcrafted 2-layer MLP, manual weight matrices, forward pass, shape printing.
- **Phase 02 — Tensor Shape Reasoning:** Formal shape contracts, input/output dimensions, byte volume calculations.
- **Phase 03 — Dtypes & Precision:** FP32, FP16, BF16, INT8. Exponent, mantissa, dynamic range, and throughput.
- **Phase 04 — Tensor Memory Layout:** Memory storage, strides, views, contiguous layout vs non-contiguous layout.
- **Phase 05 — Matrix Multiplication Cost:** FLOP calculation ($2MNK$), CPU/GPU elapsed time, roofline intuition.
- **Phase 06 — Memory vs Compute Bounds:** Arithmetic intensity ($\text{FLOPs} / \text{Byte}$), memory bandwidth saturation.
- **Phase 07 — Transformer Inference Trace:** Step-by-step trace: token ids $\to$ embeddings $\to$ attention $\to$ MLP $\to$ logits.
- **Phase 08 — Attention From First Principles:** $QK^T / \sqrt{d_k}$, softmax, scaling, sequence length memory scaling ($O(N^2)$).
- **Phase 09 — Autoregressive Generation:** Naive autoregressive generation loop, observing quadratic repeated compute.
- **Phase 10 — KV Cache Motivation:** Key/Value caching across generation steps. Eliminating redundant prompt recomputation.
- **Phase 11 — Prefill vs Decode:** Latency & throughput divergence: compute-bound prefill vs memory-bound decode.

### PART II — COMPILERS FROM FIRST PRINCIPLES
- **Phase 12 — Why AI Compilers Exist:** Overhead of eager Python dispatch, temporary memory traffic, kernel launch tax.
- **Phase 13 — Computation Graphs:** Representing mathematical operations as directed acyclic graphs (DAGs).
- **Phase 14 — Graph Execution (`mini_graph_runtime.py`):** Topological interpreter evaluating graph nodes.
- **Phase 15 — Graph Optimization:** Dead node elimination and constant folding compiler passes.
- **Phase 16 — Common Subexpression Elimination (CSE):** Detecting and merging duplicate subtrees in computation graphs.
- **Phase 17 — Operator Fusion:** Fusing adjacent elementwise ops (Add + ReLU) to eliminate DRAM traffic.
- **Phase 18 — Intermediate Representation (IR):** Linearized and structured IR representations bridging high and low level.
- **Phase 19 — SSA Intuition:** Static Single Assignment (%0, %1, %2), immutability and compiler dependency analysis.
- **Phase 20 — Compiler Passes:** Pass manager pipeline running sequentially over IR.
- **Phase 21 — Pattern Rewriting:** Pattern matchers (`x * 1 -> x`, `x + 0 -> x`, Conv+BatchNorm fusion).
- **Phase 22 — Canonicalization:** Normalizing algebraically equivalent syntax before running optimization passes.
- **Phase 23 — Shape Propagation:** Symbolic and static shape inference engine propagating shapes through tensor graphs.
- **Phase 24 — Static vs Dynamic Shapes:** Tradeoffs between specialized fixed shapes and polymorphic dynamic kernels.
- **Phase 25 — Graph Breaks:** Python dynamic behavior breaking graph capture: data-dependent control flow.
- **Phase 26 — Introduce `torch.compile`:** Comparing eager execution against TorchDynamo + TorchInductor.
- **Phase 27 — TorchDynamo Mental Model:** Bytecode interception, frame evaluation, guards, and FX graph capture.
- **Phase 28 — Guards and Recompilation:** Triggering guard failures via shape and dtype variations; recompilation cost.
- **Phase 29 — Compiler Backend:** Distinguishing graph capture frontends from hardware codegen backends.
- **Phase 30 — TorchInductor:** Inspecting Inductor generated C++/Triton code and loop scheduling.
- **Phase 31 — MLIR Motivation:** Multi-Level Intermediate Representation: bridging frameworks to hardware targets.
- **Phase 32 — MLIR Dialects:** Abstraction levels (Tensor, Linalg, Affine, LLVM dialects).
- **Phase 33 — MLIR Operations:** Anatomy of an MLIR op: operands, results, regions, attributes, and types.
- **Phase 34 — MLIR Passes and Rewriting:** Reusable dialect conversion infrastructure and pattern rewriters.
- **Phase 35 — Lowering:** Progressively lowering high-level tensor abstractions to structured loops and machine instructions.
- **Phase 36 — Hardware-Aware Compilation:** Specializing execution strategies for CPU vector registers vs GPU SIMT cores.

### PART III — GPU KERNELS & HARDWARE MODELING
- **Phase 37 — GPU Execution Model:** Host-to-device transfers, grids, thread blocks, warps, and SIMT execution.
- **Phase 38 — Kernel Launch Overhead:** Profiling latency penalty of launching many small kernels vs fused kernels.
- **Phase 39 — Memory Hierarchy:** Register file, Shared Memory / SRAM, L2 cache, HBM / DRAM transfer costs.
- **Phase 40 — Coalesced Memory Access:** Warp memory transaction coalescing vs strided non-coalesced stalls.
- **Phase 41 — Tiling:** Partitioning large matrices into cache-sized sub-blocks (CPU and GPU simulation).
- **Phase 42 — Fused Kernels:** Implementing a single-pass Matmul + Bias + Activation operator.
- **Phase 43 — Introduce Triton:** The Triton programming model: block-level pointers and automatic memory scheduling.
- **Phase 44 — Triton Vector Addition:** First Triton kernel: program ID, block pointers, mask handling, benchmarking.
- **Phase 45 — Triton Fused Activation:** Fused Linear + GELU kernel reducing global memory roundtrips.
- **Phase 46 — Triton Softmax:** Numerically stable parallel online softmax kernel.
- **Phase 47 — Triton Matrix Multiplication:** 2D block-tiled GEMM with accumulator loops and shared memory pipelining.
- **Phase 48 — Kernel Correctness:** Rigorous tolerance validation against PyTorch FP32/FP16 baselines.
- **Phase 49 — Numerical Error & Stability:** FP16 overflow, BF16 precision loss, catastrophic cancellation.
- **Phase 50 — Kernel Benchmarking:** Methodology: warmups, device synchronization, median, p95, memory throughput (GB/s).

### PART IV — INFERENCE OPTIMIZATION & SERVING
- **Phase 51 — Inference Performance Model:** Dissecting TTFT (Time To First Token), ITL (Inter-Token Latency), and tokens/sec.
- **Phase 52 — Batch Inference:** Amortizing model weight memory loads across multiple concurrent requests.
- **Phase 53 — Static Batching Bottleneck:** The padding bubble problem: stragglers stall the entire batch.
- **Phase 54 — Continuous Batching Simulator:** Dynamic iteration-level scheduling: requests enter and exit each step.
- **Phase 55 — KV Cache Memory Accounting:** Calculating memory footprint: $2 \times \text{layers} \times \text{seq} \times \text{heads} \times d_k \times \text{bytes}$.
- **Phase 56 — KV Cache Fragmentation:** Internal and external memory fragmentation in contiguous buffer allocation.
- **Phase 57 — Paged KV Cache:** Virtual memory-style block allocation (PagedAttention simulation).
- **Phase 58 — Prefix Caching:** Hash-indexed caching of repeated system prompt tokens across user queries.
- **Phase 59 — Quantization Motivation:** Memory bandwidth wall: calculating memory requirements for 7B/70B models.
- **Phase 60 — Quantization From First Principles:** Scale and zero-point mapping from $\mathbb{R} \to \mathbb{Z}$, quantize/dequantize.
- **Phase 61 — Weight-Only Quantization:** Symmetric INT8 weight-only linear layer simulation.
- **Phase 62 — INT8 vs INT4 Concepts:** Groupwise scaling, sub-byte packing, activation outlier challenges.
- **Phase 63 — Calibration:** Post-Training Quantization (PTQ) activation calibration over representative datasets.
- **Phase 64 — Quantization Error Evaluation:** Evaluating perplexity and downstream task accuracy regressions after quantization.
- **Phase 65 — Speculative Decoding:** Draft model proposes $K$ tokens; target model verifies concurrently via tree masking.
- **Phase 66 — Tensor Parallelism:** Row and Column linear sharding with All-Reduce communications.
- **Phase 67 — Pipeline Parallelism:** Layer partitioning across GPUs, 1F1B scheduling, pipeline bubbles.
- **Phase 68 — Data Parallel Inference:** Independent model replicas with load balancing across GPU workers.
- **Phase 69 — Introduce vLLM Engine:** Mapping our manual schedulers, paging, and caches to modern production vLLM.
- **Phase 70 — Serving Benchmark:** Load-testing serving engines: measuring TTFT, throughput, and p99 under concurrent load.

### PART V — TRAINING FROM FIRST PRINCIPLES
- **Phase 71 — Training Loop:** Writing the raw training step: `forward -> loss -> backward -> step -> zero_grad`.
- **Phase 72 — Cross-Entropy Loss:** Implementing log-sum-exp, one-hot indexing, and loss calculation from scratch.
- **Phase 73 — Autograd Internals:** Inspecting computation graphs, `grad_fn`, tensor gradient tracking, detaching.
- **Phase 74 — Optimizers From Scratch:** Implementing SGD with momentum and AdamW (first/second moments, bias correction).
- **Phase 75 — Training Memory Accounting:** Accounting for weights (1x), grads (1x), Adam state (2x), and activations.
- **Phase 76 — Gradient Accumulation:** Simulating larger effective batch sizes without incurring activation memory limits.
- **Phase 77 — Mixed Precision Training:** FP16/BF16 forward pass, loss scaling, master FP32 weights.
- **Phase 78 — Gradient Clipping:** Detecting exploding gradients, norm calculation, and adaptive clipping.
- **Phase 79 — Checkpointing & State Dumps:** Atomic saving and resuming of model weights, optimizer state, and RNG seed.
- **Phase 80 — Reproducibility & Non-Determinism:** Seeds, cuDNN deterministic flags, hardware non-determinism realities.

### PART VI — FINE-TUNING & MODEL ADAPTATION
- **Phase 81 — Why Fine-Tune?:** Decision matrix: Prompting vs Retrieval vs Tools vs Fine-Tuning.
- **Phase 82 — Dataset Design:** Designing high-signal instructional datasets: input, target output, metadata schemas.
- **Phase 83 — Data Cleaning:** Automated heuristic filtering: deduplication, schema validation, length truncation.
- **Phase 84 — Train / Val / Test Split Discipline:** Preventing evaluation data leakage across splits.
- **Phase 85 — Data Contamination Lab:** Demonstrating how evaluation leakages produce catastrophically false metrics.
- **Phase 86 — Instruction & Chat Formatting:** ChatML, Llama-3, and Mistral message templating; formatting errors.
- **Phase 87 — Tokenization & Sequence Length:** Analyzing token distributions, choosing padding strategies and max lengths.
- **Phase 88 — Sample Packing:** Concatenating multiple short sequences into a single context window with attention masking.
- **Phase 89 — Supervised Fine-Tuning (SFT):** Fine-tuning a small model on instruction-following datasets.
- **Phase 90 — Evaluate Before & After:** Establishing pre-training baselines on held-out tasks to quantify genuine gains.
- **Phase 91 — Overfitting Lab:** Deliberately overtraining on tiny data: train loss falls to zero while validation diverges.
- **Phase 92 — Catastrophic Forgetting:** Measuring regression on out-of-domain general knowledge benchmarks.
- **Phase 93 — Full Fine-Tuning Costs:** Quantifying the prohibitive parameter and optimizer memory footprint of full fine-tuning.
- **Phase 94 — Low-Rank Matrix Updates:** Mathematical formulation: $\Delta W = A \times B$ where $r \ll \min(d_{in}, d_{out})$.
- **Phase 95 — LoRA From First Principles:** Implementing a LoRALinear layer: frozen $W_0$, trainable $A$ and $B$, scaling $\alpha/r$.
- **Phase 96 — PEFT Library Integration:** Using Hugging Face `peft` to inject LoRA adapters into multi-head attention.
- **Phase 97 — Merge and Unmerge Adapters:** Fusing adapter weights $W = W_0 + \frac{\alpha}{r}AB$ for zero-latency inference.
- **Phase 98 — Multiple Adapters:** Hot-swapping task adapters on top of a single shared base model in memory.
- **Phase 99 — Quantized Fine-Tuning Motivation:** The memory wall: freezing base models in 4-bit while training FP16 adapters.
- **Phase 100 — QLoRA Concepts:** NormalFloat4 (NF4), double dequantization, and paged optimizers explained.
- **Phase 101 — Hyperparameter Sensitivity:** Isolating learning rate, rank $r$, alpha $\alpha$, batch size, and scheduler.
- **Phase 102 — Fine-Tuning Failure Lab:** Diagnosing training failures: LR collapse, prompt template mismatch, label leak.

### PART VII — PREFERENCE OPTIMIZATION
- **Phase 103 — Why Supervised Data Is Not Enough:** The limit of imitation learning: subtle nuances, verbosity, and preferences.
- **Phase 104 — Preference Dataset Construction:** Triplet representations: prompt ($x$), chosen ($y_w$), rejected ($y_l$).
- **Phase 105 — Reward Modeling Intuition:** Bradley-Terry model: training a scalar reward model on pairwise rankings.
- **Phase 106 — DPO From First Principles:** Direct Preference Optimization: expressing the reward implicitly via policy and reference.
- **Phase 107 — DPO Practical Lab:** Training an adapter with `DPOTrainer` and evaluating win rates against the SFT baseline.
- **Phase 108 — Online RL-Style Training Concepts:** Policy gradients, rollout generation, reward computation, PPO updates.
- **Phase 109 — GRPO / Contemporary RL Methods:** Group Relative Policy Optimization: normalizing rewards within sampled groups.
- **Phase 110 — Reward Hacking Lab:** Injecting a flawed reward proxy (e.g., length reward) and observing pathological policy outputs.
- **Phase 111 — Alignment Evaluation:** Multi-dimensional evaluations: helpfulness, truthfulness, safety boundaries, toxicity.

### PART VIII — MODEL EVALUATION RIGOR
- **Phase 112 — Evaluation Before Optimization:** Establishing the baseline contract before touching a single line of model code.
- **Phase 113 — Deterministic Evaluations:** Exact match, normalized token F1, JSON schema validation, unit test runners.
- **Phase 114 — Semantic Evaluations:** Embedding similarity, BERTScore, and reference-guided grading.
- **Phase 115 — LLM-as-Judge & Bias Mitigation:** Building an LLM judge; measuring and neutralizing position and verbosity biases.
- **Phase 116 — Human Evaluation & Rubrics:** Designing annotation rubrics, computing inter-annotator agreement (Cohen's Kappa).
- **Phase 117 — Pairwise Blind Evaluation:** Blinded, randomized pairwise comparisons with confidence intervals.
- **Phase 118 — Regression Test Suite:** Automated gating suite preventing regressions across critical business tasks.
- **Phase 119 — Slice Evaluation:** Dissecting performance across input length, domain categories, and edge cases.
- **Phase 120 — Statistical Significance:** Calculating Wilson score intervals, p-values, and statistical power for AI evals.

### PART IX — AGENTS FROM FIRST PRINCIPLES
- **Phase 121 — Model vs Agent:** The boundary: models predict tokens; agents execute control loops and mutate environment state.
- **Phase 122 — Build Manual Agent Loop:** Writing the pure Python `while not done:` loop without any framework.
- **Phase 123 — Structured Outputs & Validation:** Enforcing JSON outputs, handling malformed syntax, retrying with error feedback.
- **Phase 124 — Tool Calling Mechanics:** Function calling: extracting tool name, deserializing JSON arguments, calling functions.
- **Phase 125 — Tool Schema Engineering:** Writing unambiguous, strict schemas (types, constraints, explicit docstrings).
- **Phase 126 — Tool Argument Validation:** Defensive boundary: type casting, range validation, authorization checks.
- **Phase 127 — Tool Error Handling:** Handling tool exceptions, network timeouts, and partial errors gracefully.
- **Phase 128 — Agent State Management:** Disentangling conversation messages, working scratchpad, and environment state.
- **Phase 129 — Context Window as a Finite Resource:** Measuring token consumption, degradation of reasoning under long contexts.
- **Phase 130 — Context Management Strategies:** Selection, rolling truncation, recursive summarization, and RAG injection.
- **Phase 131 — Long-Term Memory:** Dissecting model weights vs prompt context vs external persistent key-value memory.
- **Phase 132 — Memory Retrieval:** Semantic search over user memories; measuring false positive memory retrievals.
- **Phase 133 — Memory Updating & Invalidation:** Handling conflicting memories, versioning facts, deleting stale facts.

### PART X — RETRIEVAL SYSTEMS (RAG)
- **Phase 134 — Why Retrieval?:** Private data, freshness, and reducing hallucination without retraining.
- **Phase 135 — Lexical / Keyword Search:** Inverted index and BM25 scoring from first principles.
- **Phase 136 — Vector Embeddings:** Mapping text into high-dimensional latent space; embedding geometry and cosine distance.
- **Phase 137 — Vector Similarity Search:** Exact brute-force kNN vs approximate nearest neighbor (HNSW intuition).
- **Phase 138 — Chunking Strategies:** Fixed character chunks vs sliding windows vs sentence/semantic chunk boundaries.
- **Phase 139 — Metadata Filtering:** Pre-filtering by tenant ID, date range, and document classification before search.
- **Phase 140 — Hybrid Search:** Reciprocal Rank Fusion (RRF) combining dense vector similarity with sparse BM25.
- **Phase 141 — Reranking:** Cross-encoder rerankers scoring candidate passages; measuring latency vs NDCG gains.
- **Phase 142 — RAG Pipeline:** Complete pipeline: ingestion $\to$ chunking $\to$ indexing $\to$ retrieval $\to$ synthesis.
- **Phase 143 — Retrieval Failure Decomposition:** Isolating failure: Did retrieval miss? Was noise returned? Did model ignore?
- **Phase 144 — Citations & Provenance:** Grounding responses in retrieved chunks; detecting fabricated citations.

### PART XI — WORKFLOWS & ORCHESTRATION
- **Phase 145 — Deterministic Workflow vs Agent:** The autonomy spectrum: when ordinary deterministic code is superior to an LLM.
- **Phase 146 — Workflow State Machine:** Building an explicit Finite State Machine (FSM) where models govern select transitions.
- **Phase 147 — Semantic Router:** Fast embedding-based or small-model classification routing user queries to bounded handlers.
- **Phase 148 — Planner / Executor Architecture:** Generating an upfront execution plan, sequentially evaluating steps, and replanning.
- **Phase 149 — Loop Limits & Circuit Breakers:** Hard iteration caps, token expenditure limits, and infinite loop detectors.
- **Phase 150 — Agent Handoffs:** Structured control transfer between specialized agents with explicit state handoff contracts.
- **Phase 151 — Multi-Agent Skepticism:** Debunking "agent swarms"; measuring token bloat and error amplification vs single agent.
- **Phase 152 — Multi-Agent Communication:** Strict communication protocols: preventing unconstrained agent-to-agent chatter.
- **Phase 153 — Introduce Agent SDK:** Mapping our manual agent loops, tools, and routers to production SDKs.
- **Phase 154 — Framework Escape Hatch:** Deconstructing a framework agent into its manual equivalent to debug production hangs.

### PART XII — AGENT SECURITY & TRUST BOUNDARIES
- **Phase 155 — Prompt Injection:** Direct adversarial overrides: extracting system instructions and altering logic.
- **Phase 156 — Indirect Prompt Injection:** Untrusted documents and web pages hijacking agent execution flow.
- **Phase 157 — Tool Permission Boundaries:** Implementing least privilege: restricting dangerous system capabilities.
- **Phase 158 — Read vs Write Tools:** Enforcing distinct authorization pipelines for queries vs external state mutations.
- **Phase 159 — Human-in-the-Loop Approval:** Two-phase commit: agent proposes high-stakes action; user approves before execution.
- **Phase 160 — Execution Sandboxing:** Running code generation tools in restricted ephemeral containers (memory, CPU, network caps).
- **Phase 161 — Secret Isolation:** Preventing API keys, passwords, and sensitive session tokens from entering model context.
- **Phase 162 — Multi-Tenant Authorization:** Enforcing tenant data isolation in deterministic application code, not prompts.
- **Phase 163 — Data Exfiltration Defenses:** Blocking exfiltration channels (markdown image beacons, outbound webhook abuse).

### PART XIII — PRODUCTION AGENT RELIABILITY
- **Phase 164 — Model Calls Fail:** Simulating 429 rate limits, 503 service outages, connection timeouts, and empty responses.
- **Phase 165 — Timeouts & Deadlines:** Context-aware request deadlines propagating across nested tool and model invocations.
- **Phase 166 — Safe Retries:** Differentiating idempotent read operations from non-idempotent mutation operations.
- **Phase 167 — Idempotent Tool Execution:** Idempotency keys: preventing double-billing or duplicate emails on network failure.
- **Phase 168 — Exponential Backoff & Jitter:** Preventing thundering herd problem during model provider downtime.
- **Phase 169 — Fallback Models:** Graceful degradation: switching to secondary model providers when primary is unavailable.
- **Phase 170 — Dynamic Model Routing:** Routing simple queries to cheap models and complex queries to frontier models.
- **Phase 171 — Caching AI Work:** Semantic embedding cache and exact prompt cache; cache invalidation strategies.
- **Phase 172 — Rate Limiting Architecture:** Token bucket and leaky bucket algorithms bounding user and model call rates.
- **Phase 173 — Backpressure & Queueing:** Worker pools bounding concurrent LLM calls to prevent system starvation.
- **Phase 174 — Cooperative Cancellation:** Propagating user cancellation signals to abort in-flight generation and tool execution.

### PART XIV — AI OBSERVABILITY & TRACING
- **Phase 175 — Tracing an Agent Run:** End-to-end distributed tracing: tracking prompts, tools, latencies, and token counts.
- **Phase 176 — Structured AI Traces:** Emitting OpenTelemetry-compatible spans for model invocations and tool actions.
- **Phase 177 — Token Cost & Budget Accounting:** Real-time dollar metering of input, output, and cache tokens per tenant.
- **Phase 178 — Quality Monitoring Beyond HTTP 200:** Monitoring semantic correctness, schema failure rates, and drift in production.
- **Phase 179 — Agent Failure Taxonomy:** Structured categorization of production failures (model, tool, schema, timeout, policy).
- **Phase 180 — Root-Cause Debugging:** Step-by-step diagnostic workflow: isolating whether failure is model, data, tool, or code.

### PART XV — PRODUCTION EVALUATION GATES
- **Phase 181 — Offline Evaluation Harness:** Automated test runner executing regression suites against staging models.
- **Phase 182 — Online Evaluation & Telemetry:** Sampling production traffic for continuous human and judge scoring with PII redaction.
- **Phase 183 — Shadow Deployments:** Dual-running new models against live user traffic without impacting user responses.
- **Phase 184 — A/B Testing AI Features:** Conducting randomized experiments measuring true business KPIs, not just LLM scores.
- **Phase 185 — Canary Deployments:** Routing 1% of live traffic to fine-tuned adapters; monitoring latency and error spikes.
- **Phase 186 — Automated Deployment Gates:** CI/CD pipeline blocking releases if accuracy, latency, or cost regressions occur.

### PART XVI — END-TO-END SYSTEM PERFORMANCE
- **Phase 187 — End-to-End Latency Budgeting:** Allocating budgets: network, retrieval, TTFT, generation, tool calls.
- **Phase 188 — Token Economics:** Analyzing the marginal latency, dollar, and memory costs of bloated prompts.
- **Phase 189 — Context Optimization:** Pruning extraneous instructions and examples to optimize cost and latency.
- **Phase 190 — Model Size Tradeoffs:** Quantifying 1B vs 7B vs 70B across accuracy, TTFT, throughput, and hardware costs.
- **Phase 191 — Fine-Tuning vs Prompting vs RAG:** The ultimate comparison: evaluating all three on the exact same domain task.
- **Phase 192 — Fine-Tuned Small Model vs Frontier Model:** Benchmarking a 3B domain LoRA model against a generic frontier model.
- **Phase 193 — Serving Fine-Tuned Adapters:** Latency and memory benchmarks of loading LoRA adapters dynamically at serving time.
- **Phase 194 — Multi-Tenant Adapter Serving:** Routing requests to hundreds of customer LoRA adapters on shared base weights.

### PART XVII — BROKEN AI SYSTEMS (40+ LABS)
- **Phase 195 — Broken Compiler Lab:** Diagnosing why `torch.compile` runs slower than eager execution (graph breaks, warmup).
- **Phase 196 — Broken Kernel Lab:** Debugging a Triton kernel that runs fast but produces catastrophic numerical inaccuracy.
- **Phase 197 — Broken Fine-Tune Lab:** Diagnosing training loss collapse accompanied by validation loss explosion.
- **Phase 198 — Broken LoRA Lab:** Debugging an adapter that trains without error but produces zero behavioral change.
- **Phase 199 — Broken Quantization Lab:** Investigating why INT4 quantization destroyed reasoning on mathematical tasks.
- **Phase 200 — Broken Serving Lab:** Diagnosing why p99 latency spiked 50x under concurrent continuous batching.
- **Phase 201 — Broken Retrieval Lab:** Uncovering why a RAG agent hallucinated when retrieval fetched irrelevant noise.
- **Phase 202 — Broken Agent Tool Lab:** Debugging an agent generating invalid JSON parameters despite clear docstrings.
- **Phase 203 — Broken Agent Loop Lab:** Rescuing an agent stuck in an infinite tool-calling loop burning API budget.
- **Phase 204 — Broken Security Lab:** Exploiting and fixing an indirect prompt injection in a customer support workflow.
- **Phase 205 — Duplicate Side-Effect Lab:** Debugging a payment tool that billed a customer twice after a network retry.
- **Phase 206 — Context Explosion Lab:** Debugging a multi-turn conversation that crashed the inference engine with an OOM.
- **Phase 207 — Master Broken AI Systems Suite:** 40+ isolated diagnostic challenges covering the entire engineering stack.

### PART XVIII — SUBSTANTIAL PROJECTS (15 PROJECTS)
- **Phase 208 — Project: Mini Tensor Compiler:** Graph builder, IR emitter, constant folding, dead-node elimination, and runtime.
- **Phase 209 — Project: Tiny MLIR-Style IR:** Multi-level IR with dialects, types, operations, and lowering passes.
- **Phase 210 — Project: Triton Kernel Pack:** Vector addition, GELU activation, RMSNorm, and 2D tiled GEMM kernels.
- **Phase 211 — Project: Mini Inference Scheduler:** Priority queue, prefill/decode separation, continuous batching simulator.
- **Phase 212 — Project: Quantized Model Experiment:** Comprehensive benchmark comparing FP32, FP16, INT8, and INT4.
- **Phase 213 — Project: Fine-Tune a Domain Model:** End-to-end pipeline: dataset cleaning, baseline eval, LoRA, and serving.
- **Phase 214 — Project: Preference Optimization:** Constructing preference pairs, training with DPO, and measuring win rate.
- **Phase 215 — Project: Evaluation Harness:** Reusable eval framework: deterministic tests, LLM judge, and regression gates.
- **Phase 216 — Project: Tool-Using Agent From Scratch:** Framework-free agent with schemas, validation, state, and retries.
- **Phase 217 — Project: Production RAG System:** Hybrid search (BM25 + dense), chunking, reranking, and citation tracking.
- **Phase 218 — Project: Research Agent:** Multi-turn query decomposition, provenance tracking, and budget circuit breakers.
- **Phase 219 — Project: Coding Agent Sandbox:** Sandboxed code execution agent with resource caps, test runners, and git rollbacks.
- **Phase 220 — Project: Customer Support Agent:** Read-only retrieval, human-in-the-loop escalation, policy adherence.
- **Phase 221 — Project: Data Analysis Agent:** Safe SQL generation, pandas sandbox execution, and chart verification.
- **Phase 222 — Project: Multi-Agent Workflow:** Deterministic orchestrator coordinating researcher, writer, and editor agents.

### PART XIX — CAPSTONES & FINAL CHALLENGE
- **Phase 223 — Capstone 1: Compile and Serve a Model:** Compiling, quantizing, and load-testing a model with latency profiling.
- **Phase 224 — Capstone 2: Local Fine-Tuning Platform:** End-to-end CLI for dataset validation, LoRA training, checkpointing, and evals.
- **Phase 225 — Capstone 3: Production Agent Platform:** Production API gateway, auth, rate limiting, tracing, and sandboxed tools.
- **Phase 226 — Capstone 4: Fine-Tuned Agent:** Identifying a model tool-calling flaw, training an adapter, and proving improvement.
- **Phase 227 — Capstone 5: Optimized Fine-Tuned Agent:** Complete convergence: LoRA model + optimized serving + sandboxed agent.
- **Phase 228 — Capstone 6: Failure Day (Chaos Engineering):** Injected chaos: model outages, stale indexes, injections, and recovery.
- **Phase 229 — Capstone 7: Cost Reduction:** Reducing production AI costs by 70% while protecting benchmark quality.
- **Phase 230 — Final AI Systems Challenge:** The enterprise AI assistant: end-to-end design, implementation, and deployment under strict SLAs.
