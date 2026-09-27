# Part VI — Fine-Tuning & Model Adaptation (Phases 81 – 102)

> **Motto:** A fine-tune is only as good as the learning signal. Garbage data cannot be hidden behind training frameworks.

---

## Phases 81 – 88: Dataset Engineering & Preparation
- **Phase 81 — Why Fine-Tune?:** Decision matrix: Prompting vs Retrieval vs Tools vs Fine-Tuning.
- **Phase 82 — Dataset Design:** Designing high-signal instructional datasets (`datasets/dataset_cleaner.py`).
- **Phase 83 — Data Cleaning:** Automated heuristic filtering: deduplication, schema validation, length truncation.
- **Phase 84 — Train / Val / Test Split Discipline:** Preventing evaluation data leakage across splits.
- **Phase 85 — Data Contamination Lab:** Demonstrating how evaluation leakages produce false metrics (`datasets/data_split_and_contamination.py`).
- **Phase 86 — Instruction & Chat Formatting:** ChatML, Llama-3, and Mistral message templating (`datasets/instruction_formatter.py`).
- **Phase 87 — Tokenization & Sequence Length:** Analyzing token distributions, choosing padding strategies (`datasets/sequence_length_analyzer.py`).
- **Phase 88 — Sample Packing:** Concatenating short sequences with 2D attention masks (`datasets/sample_packer.py`).

---

## Phases 89 – 93: Supervised Fine-Tuning (SFT) & Overfitting
- **Phase 89 — Supervised Fine-Tuning (SFT):** Fine-tuning on instruction-following datasets.
- **Phase 90 — Evaluate Before & After:** Establishing pre-training baselines on held-out tasks.
- **Phase 91 — Overfitting Lab:** Deliberately overtraining on tiny data: train loss falls to zero while validation diverges.
- **Phase 92 — Catastrophic Forgetting:** Measuring regression on out-of-domain general knowledge benchmarks.
- **Phase 93 — Full Fine-Tuning Costs:** Quantifying the prohibitive parameter and optimizer memory footprint of full fine-tuning.

---

## Phases 94 – 102: Low-Rank Adaptation (LoRA & QLoRA)
- **Phase 94 — Low-Rank Matrix Updates:** Mathematical formulation: $\Delta W = A \times B$ where $r \ll \min(d_{in}, d_{out})$.
- **Phase 95 — LoRA From First Principles:** Implementing a LoRALinear layer: frozen $W_0$, trainable $A$ and $B$, scaling $\alpha/r$.
- **Phase 96 — PEFT Library Integration:** Using Hugging Face `peft` to inject LoRA adapters into multi-head attention.
- **Phase 97 — Merge and Unmerge Adapters:** Fusing adapter weights $W = W_0 + \frac{\alpha}{r}AB$ for zero-latency inference.
- **Phase 98 — Multiple Adapters:** Hot-swapping task adapters on top of a single shared base model in memory.
- **Phase 99 — Quantized Fine-Tuning Motivation:** The memory wall: freezing base models in 4-bit while training FP16 adapters.
- **Phase 100 — QLoRA Concepts:** NormalFloat4 (NF4), double dequantization, and paged optimizers explained.
- **Phase 101 — Hyperparameter Sensitivity:** Isolating learning rate, rank $r$, alpha $\alpha$, batch size, and scheduler.
- **Phase 102 — Fine-Tuning Failure Lab:** Diagnosing training failures: LR collapse, prompt template mismatch, label leak.
