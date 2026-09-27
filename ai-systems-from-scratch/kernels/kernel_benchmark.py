"""
Rigorous Kernel Benchmarking Methodology (Phase 50).
Enforces:
1. Warmup iterations to trigger JIT compilation and caches.
2. Device synchronization (torch.cuda.synchronize() or torch.mps.synchronize()).
3. Measurement of median, p95 latencies, and effective memory bandwidth (GB/s).
"""

import time
import numpy as np
import torch
from typing import Callable, Dict, Any

def benchmark_custom_kernel(
    kernel_fn: Callable[[], Any],
    bytes_transferred: int,
    warmup: int = 10,
    iterations: int = 50,
    device: str = "cpu"
) -> Dict[str, float]:
    # 1. Warmup
    for _ in range(warmup):
        kernel_fn()
    
    if device == "cuda":
        torch.cuda.synchronize()
    elif device == "mps" and hasattr(torch, "mps"):
        torch.mps.synchronize()

    # 2. Measurement iterations
    latencies_ms = []
    for _ in range(iterations):
        t0 = time.perf_counter()
        kernel_fn()
        if device == "cuda":
            torch.cuda.synchronize()
        elif device == "mps" and hasattr(torch, "mps"):
            torch.mps.synchronize()
        t1 = time.perf_counter()
        latencies_ms.append((t1 - t0) * 1000.0)

    median_lat = float(np.median(latencies_ms))
    p95_lat = float(np.percentile(latencies_ms, 95))
    
    # Bandwidth in GB/s = (bytes transferred) / (seconds) / 1e9
    bandwidth_gb_s = (bytes_transferred / (median_lat / 1000.0)) / 1e9 if median_lat > 0 else 0.0

    return {
        "median_ms": median_lat,
        "p95_ms": p95_lat,
        "bandwidth_gb_s": bandwidth_gb_s,
        "iterations": iterations
    }
