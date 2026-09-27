"""
Operator Fusion Lab (Phase 17).
Demonstrates how eager execution materializes intermediate tensors in DRAM/RAM,
whereas operator fusion keeps intermediate activations in registers, eliminating
memory bandwidth overhead and kernel launch latency.
"""

import time
import numpy as np
import torch

def eager_add_relu(x: torch.Tensor, bias: torch.Tensor) -> torch.Tensor:
    """
    Eager execution:
    1. Kernel 1: y = x + bias -> writes intermediate 'y' to memory.
    2. Kernel 2: out = relu(y) -> reads 'y' from memory, writes 'out' to memory.
    Total memory traffic: 2 reads, 2 writes for y!
    """
    y = x + bias
    out = torch.relu(y)
    return out

def fused_add_relu_primitive(x: np.ndarray, bias: np.ndarray) -> np.ndarray:
    """
    From-scratch primitive: Single pass elementwise fusion.
    Loads x[i] and bias[i] directly into CPU registers, computes sum,
    applies max(0, val), and writes output directly.
    Zero intermediate memory allocations.
    """
    out = np.empty_like(x)
    # Using flatiter to simulate a single hardware SIMD/loop kernel
    it_x = np.nditer(x)
    it_b = np.nditer(bias)
    it_o = np.nditer(out, op_flags=['readwrite'])
    
    while not it_x.finished:
        val = it_x[0] + it_b[0]
        it_o[0] = val if val > 0 else 0
        it_x.iternext()
        it_b.iternext()
        it_o.iternext()
    return out

@torch.compile
def compiled_fused_add_relu(x: torch.Tensor, bias: torch.Tensor) -> torch.Tensor:
    """
    PyTorch 2.x TorchInductor fused kernel.
    Inductor generates a single fused C++ OpenMP or Triton kernel.
    """
    return torch.relu(x + bias)

def compare_fusion_memory_and_speed():
    size = 2_000_000
    x = torch.randn(size, dtype=torch.float32)
    b = torch.randn(size, dtype=torch.float32)
    
    # Warmup
    for _ in range(5):
        _ = eager_add_relu(x, b)
        _ = compiled_fused_add_relu(x, b)
        
    t0 = time.perf_counter()
    for _ in range(50):
        res_eager = eager_add_relu(x, b)
    t_eager = (time.perf_counter() - t0) * 1000.0 / 50.0
    
    t0 = time.perf_counter()
    for _ in range(50):
        res_fused = compiled_fused_add_relu(x, b)
    t_fused = (time.perf_counter() - t0) * 1000.0 / 50.0
    
    # Correctness check
    assert torch.allclose(res_eager, res_fused, atol=1e-5)
    
    # Memory traffic calculation:
    # Eager: Read x (8MB), Read b (8MB), Write temp (8MB), Read temp (8MB), Write out (8MB) = 40MB
    # Fused: Read x (8MB), Read b (8MB), Write out (8MB) = 24MB (40% reduction in memory traffic!)
    bytes_eager = 5 * (size * 4)
    bytes_fused = 3 * (size * 4)
    traffic_saved_mb = (bytes_eager - bytes_fused) / (1024 * 1024)
    
    return {
        "eager_ms": t_eager,
        "fused_ms": t_fused,
        "speedup": t_eager / t_fused if t_fused > 0 else 1.0,
        "memory_traffic_saved_mb": traffic_saved_mb
    }

if __name__ == "__main__":
    results = compare_fusion_memory_and_speed()
    print("Operator Fusion Results:", results)
