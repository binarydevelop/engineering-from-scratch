#!/usr/bin/env python3
"""
GPU / Accelerator Inspector for AI Systems Engineering.
Reports hardware device details, peak memory, bandwidth theoretical bounds,
and determines Tier 1 (CPU), Tier 2 (Single GPU), or Tier 3 (Multi-GPU).
"""

import sys
import os

try:
    import torch
except ImportError:
    print("PyTorch is not installed. Run 'make setup' first.")
    sys.exit(1)

def inspect_accelerator():
    print("=" * 60)
    print(" AI Systems Engineering - Hardware & Accelerator Report")
    print("=" * 60)
    
    cuda_avail = torch.cuda.is_available()
    mps_avail = hasattr(torch.backends, "mps") and torch.backends.mps.is_available()
    
    if cuda_avail:
        device_count = torch.cuda.device_count()
        print(f"CUDA Status: DETECTED ({device_count} device{'s' if device_count > 1 else ''})")
        for i in range(device_count):
            props = torch.cuda.get_device_properties(i)
            mem_gb = props.total_memory / (1024 ** 3)
            print(f"  Device {i}: {props.name}")
            print(f"    Compute Capability : {props.major}.{props.minor}")
            print(f"    Total Memory       : {mem_gb:.2f} GB")
            print(f"    Multi-Processors   : {props.multi_processor_count}")
        
        tier = "Tier 3 (Multi-GPU)" if device_count > 1 else "Tier 2 (Single GPU)"
        print(f"\nRecommended Course Hardware Tier: {tier}")
        print("Supported Labs: All Tier 1 + Tier 2 + Triton Kernels + Local SFT/LoRA + INT4 Quantization.")
        
    elif mps_avail:
        print("Apple Silicon MPS Status: DETECTED")
        print("  Backend: Metal Performance Shaders (torch.device('mps'))")
        print("Recommended Course Hardware Tier: Tier 1+ (CPU + MPS Accelerated Tensors)")
        print("Supported Labs: All CPU labs + MPS matrix multiplications + PyTorch SFT/LoRA.")
        print("Note: Triton GPU kernels and torch.compile Inductor CUDA codegen require Linux/CUDA.")
        print("      Mac users utilize the CPU/PyTorch simulation equivalents for Triton/Inductor phases.")
        
    else:
        print("Accelerator Status: NO GPU DETECTED (CPU Mode)")
        print("Recommended Course Hardware Tier: Tier 1 (CPU)")
        print("Supported Labs: All foundational tracks, tiny transformer, compiler graph IRs,")
        print("                CPU tiled matmul, manual training loop, manual agent loop,")
        print("                evaluations, security, and simulated scheduling.")
    
    print("-" * 60)
    # Quick tensor test
    device = torch.device("cuda:0" if cuda_avail else ("mps" if mps_avail else "cpu"))
    x = torch.randn(1024, 1024, device=device)
    y = torch.randn(1024, 1024, device=device)
    z = torch.matmul(x, y)
    print(f"Quick Tensor Test: Matmul [1024, 1024] on '{device}' succeeded. Output sum: {z.sum().item():.2f}")
    print("=" * 60)

if __name__ == "__main__":
    inspect_accelerator()
