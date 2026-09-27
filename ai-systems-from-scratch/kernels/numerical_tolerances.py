"""
Numerical Error & Tolerances Lab (Phases 48-49).
Explores dynamic range, precision bits, and machine epsilon across
FP32, FP16, and BF16, and demonstrates why fast wrong kernels fail.
"""

from typing import Dict, Tuple
import torch

def inspect_dtype_characteristics() -> Dict[str, Dict]:
    dtypes = {
        "float32": torch.float32,
        "float16": torch.float16,
        "bfloat16": torch.bfloat16
    }
    info = {}
    for name, dt in dtypes.items():
        finfo = torch.finfo(dt)
        info[name] = {
            "bits": finfo.bits,
            "mantissa_bits": finfo.mantissa,
            "max": finfo.max,
            "min": finfo.min,
            "eps": finfo.eps,
            "tiny": finfo.tiny
        }
    return info

def compare_precision_loss(size: int = 1000) -> Dict[str, float]:
    """
    Demonstrates catastrophic precision loss and cancellation:
    Adding small numbers to large numbers in FP16 vs FP32 vs BF16.
    """
    # Large number + many small numbers
    large_val = 10000.0
    small_val = 0.001

    # In FP32
    acc_fp32 = torch.tensor(large_val, dtype=torch.float32)
    delta_fp32 = torch.tensor(small_val, dtype=torch.float32)
    for _ in range(size):
        acc_fp32 += delta_fp32

    # In FP16
    acc_fp16 = torch.tensor(large_val, dtype=torch.float16)
    delta_fp16 = torch.tensor(small_val, dtype=torch.float16)
    for _ in range(size):
        acc_fp16 += delta_fp16

    # In BF16
    acc_bf16 = torch.tensor(large_val, dtype=torch.bfloat16)
    delta_bf16 = torch.tensor(small_val, dtype=torch.bfloat16)
    for _ in range(size):
        acc_bf16 += delta_bf16

    true_val = large_val + (size * small_val)
    return {
        "expected_true": true_val,
        "fp32_result": acc_fp32.item(),
        "fp32_abs_error": abs(acc_fp32.item() - true_val),
        "fp16_result": acc_fp16.item(),
        "fp16_abs_error": abs(acc_fp16.item() - true_val),
        "bf16_result": acc_bf16.item(),
        "bf16_abs_error": abs(acc_bf16.item() - true_val)
    }

def verify_kernel_correctness(actual: torch.Tensor, expected: torch.Tensor, dtype: torch.dtype) -> Tuple[bool, float, float]:
    """
    Rigorous tolerance checker adhering to standard PyTorch tolerances:
    - FP32: rtol=1e-4, atol=1e-5
    - FP16: rtol=1e-3, atol=1e-3
    - BF16: rtol=1e-2, atol=1e-2
    """
    if dtype == torch.float32:
        rtol, atol = 1e-4, 1e-5
    elif dtype == torch.float16:
        rtol, atol = 1e-3, 1e-3
    elif dtype == torch.bfloat16:
        rtol, atol = 1e-2, 1e-2
    else:
        rtol, atol = 1e-5, 1e-5

    max_abs_diff = torch.max(torch.abs(actual - expected)).item()
    relative_diff = torch.max(torch.abs(actual - expected) / (torch.abs(expected) + 1e-8)).item()
    is_close = torch.allclose(actual, expected, rtol=rtol, atol=atol)
    return is_close, max_abs_diff, relative_diff
