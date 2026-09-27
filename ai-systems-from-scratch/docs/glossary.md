# AI Systems Engineering Glossary

A rigorous reference defining foundational terms across compilers, inference runtimes, model adaptation, and agent architectures.

---

| Term | What People Say / Common Misconception | Actual Systems Engineering Definition |
| :--- | :--- | :--- |
| **Arithmetic Intensity** | "How fast a model runs." | The ratio of arithmetic operations (FLOPs) to memory traffic (Bytes transferred from DRAM): $\text{Intensity} = \frac{\text{FLOPs}}{\text{Bytes}}$. Governs whether an operation is compute-bound or memory-bound on the Roofline model. |
| **Graph Break** | "When PyTorch crashes." | An event during `torch.compile` where TorchDynamo encounters unsupported Python bytecode (e.g. data-dependent Python control flow or unsupported C extensions), forcing execution back to the slow eager Python interpreter. |
| **Operator Fusion** | "Combining two functions." | A compiler optimization that merges multiple adjacent operations into a single machine kernel, eliminating intermediate memory writes to global DRAM/HBM and reducing kernel launch overhead. |
| **KV Cache** | "A Redis cache for prompts." | A contiguous or paged GPU tensor buffer holding precomputed Key and Value projections for historical tokens, eliminating $O(S^2)$ redundant recomputation during autoregressive decoding. |
| **Continuous Batching** | "Running requests in parallel." | An iteration-level scheduling algorithm where requests enter and exit the active compute batch dynamically token-by-token, eliminating padding bubbles common in static batching. |
| **PagedAttention** | "Fancy attention math." | A virtual memory management strategy for the KV cache that partitions sequences into fixed-size physical blocks, completely eliminating external memory fragmentation. |
| **LoRA (Low-Rank Adaptation)** | "Fine-tuning on cheap hardware." | A parameter-efficient adaptation technique freezing pre-trained weights $W_0 \in \mathbb{R}^{d \times k}$ and adding a low-rank decomposition $\Delta W = B \cdot A$ ($B \in \mathbb{R}^{d \times r}, A \in \mathbb{R}^{r \times k}, r \ll \min(d, k)$), drastically reducing optimizer memory. |
| **DPO (Direct Preference Optimization)** | "RL without RL." | An alignment method that analytically solves for the optimal policy under the Bradley-Terry preference model, directly optimizing language model weights using cross-entropy on pairwise preferences without training an explicit reward model or policy gradient loop. |
| **Agent** | "A sentient AI that does things." | A deterministic software control loop (`while` loop) that repeatedly feeds external observations into a language model, validates structured tool requests against a schema, and executes actions in an environment until a termination condition is reached. |
| **Idempotency Key** | "An API security password." | A unique client-generated token attached to state-mutating requests ensuring that retried network calls do not execute the side-effect (e.g., credit card charge) more than once. |
| **Indirect Prompt Injection** | "Tricking the chatbot." | An adversarial security exploit where untrusted third-party data retrieved by a tool or RAG pipeline contains hidden instructions that hijack the model's control flow and manipulate tool execution. |
| **TTFT (Time To First Token)** | "Response time." | The elapsed time from client request submission to the emission of the first token, dominated by queue delay and prompt prefill computation. |
| **Inter-Token Latency (ITL)** | "Streaming speed." | The elapsed time between consecutive generated tokens in the autoregressive decode phase, strictly bound by GPU memory bandwidth. |
