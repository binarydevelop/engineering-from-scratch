# Part V — Training From First Principles (Phases 71 – 80)

> **Motto:** Before using high-level trainers, write the loop manually: forward, loss, backward, step, zero_grad.

---

## Phases 71 – 75: The Core Training Mechanics & Memory
- **Phase 71 — Training Loop:** Writing the raw training step without trainer frameworks (`training/manual_training_loop.py`).
- **Phase 72 — Cross-Entropy Loss:** Implementing log-sum-exp, one-hot indexing, and loss calculation from scratch (`training/cross_entropy_from_scratch.py`).
- **Phase 73 — Autograd Internals:** Inspecting computation graphs, `grad_fn`, tensor gradient tracking, detaching (`training/autograd_debugger.py`).
- **Phase 74 — Optimizers From Scratch:** Implementing SGD with momentum and AdamW from scratch (`training/custom_optimizers.py`).
- **Phase 75 — Training Memory Accounting:** Accounting for weights (1x), grads (1x), Adam state (2x), and activations (`training/memory_accounting.py`).

---

## Phases 76 – 80: Scale, Stability & Fault Tolerance
- **Phase 76 — Gradient Accumulation:** Simulating larger effective batch sizes without incurring activation memory limits (`training/gradient_accumulation.py`).
- **Phase 77 — Mixed Precision Training:** FP16/BF16 forward pass, loss scaling, master FP32 weights.
- **Phase 78 — Gradient Clipping:** Detecting exploding gradients, norm calculation, and adaptive clipping (`training/gradient_clipping.py`).
- **Phase 79 — Checkpointing & State Dumps:** Atomic saving and resuming of model weights, optimizer state, and RNG seed (`training/checkpoint_manager.py`).
- **Phase 80 — Reproducibility & Non-Determinism:** Seeds, cuDNN deterministic flags, hardware non-determinism realities.
