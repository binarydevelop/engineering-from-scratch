# The Core Mental Models of AI Systems Engineering

---

## 1. The Roofline Model: Compute vs Memory Bandwidth

Every tensor operation on any hardware device is bounded by either:
1. **Compute Throughput (TFLOPs):** The raw number of arithmetic operations the processor cores (ALUs / Tensor Cores) can execute per second.
2. **Memory Bandwidth (GB/s):** The rate at which bytes can be transferred from global DRAM/HBM to on-chip registers/SRAM.

$$\text{Attainable Performance (TFLOPs)} = \min\left(\text{Peak Compute}, \text{Arithmetic Intensity} \times \text{Memory Bandwidth}\right)$$

```text
Attainable
Performance ▲
  (TFLOPs)  │             ┌───────────────────────── Peak Compute Ceiling
            │            /  (COMPUTE BOUND: Prefill, Large GEMM)
            │           /
            │          /
            │         /
            │        / (MEMORY BOUND: Decode, Elementwise Add/ReLU)
            │       /
            │      /
            │     /
            └────┴──────────────────────────────────────►
                0        Intensity Boundary (FLOPs/Byte)     Arithmetic Intensity
```

---

## 2. The Memory Pyramid of a Modern Accelerator

Understanding physical data movement is critical for compiler and kernel reasoning:

```text
┌──────────────────────────────────────┐  Capacity: ~64KB per SM
│ Registers (Single Cycle Latency)     │  Speed: ~30 TB/s aggregate
├──────────────────────────────────────┤
│ L1 Cache / Shared Memory (SRAM)      │  Capacity: ~128–228KB per SM
│ (~10-30 cycles latency)              │  Speed: ~15 TB/s aggregate
├──────────────────────────────────────┤
│ L2 Cache (Shared Across GPU)         │  Capacity: ~50–96MB
│ (~100-200 cycles latency)            │  Speed: ~5 TB/s
├──────────────────────────────────────┤
│ Global Device Memory (HBM3 / GDDR6)  │  Capacity: 16GB – 192GB
│ (~400-800 cycles latency)            │  Speed: 1 – 3.3 TB/s
├──────────────────────────────────────┤
│ Host RAM (via PCIe Gen 4/5)          │  Capacity: 128GB – 2TB
│ (~10,000+ cycles latency)            │  Speed: 32 – 64 GB/s (MASSIVE BOTTLENECK)
└──────────────────────────────────────┘
```

**Compiler takeaway:** Moving data between Host RAM and HBM is disastrously slow. Moving data between HBM and Registers is the next biggest bottleneck. **Fusing operations keeps intermediate tensors inside Registers and SRAM!**

---

## 3. The 5 Distinctions of Memory in AI Systems

Never confuse these distinct storage domains:

1. **Model Weights:** Static neural network parameters ($\theta$) stored in HBM/RAM.
2. **Prompt Context:** Ephemeral sequence of token IDs passed into the current forward pass.
3. **KV Cache:** Transient intermediate activation tensors cached during autoregressive generation.
4. **Conversation / Working State:** Application-level structured scratchpad, turn history, and variables.
5. **Long-Term Memory / Retrieval Corpus:** Persistent external databases, vector indexes, or document stores.
