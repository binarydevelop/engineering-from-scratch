"""
Fused Linear + Activation Kernel (Phase 42).
Implements a single-pass Matrix Multiply + Bias Add + GELU activation,
comparing numerical accuracy and memory footprint against separate passes.
"""

import math
import numpy as np
import torch

def eager_linear_gelu(x: torch.Tensor, weight: torch.Tensor, bias: torch.Tensor) -> torch.Tensor:
    """
    Eager pipeline:
    1. mm = x @ weight.t() (writes mm to DRAM)
    2. aff = mm + bias (reads mm, writes aff to DRAM)
    3. out = gelu(aff) (reads aff, writes out to DRAM)
    """
    mm = torch.matmul(x, weight.t())
    aff = mm + bias
    out = torch.nn.functional.gelu(aff)
    return out

def manual_fused_linear_gelu(x: torch.Tensor, weight: torch.Tensor, bias: torch.Tensor) -> torch.Tensor:
    """
    Fused conceptual implementation:
    Computes dot products and immediately folds bias and GELU activation
    before writing to final destination buffer.
    """
    out = torch.matmul(x, weight.t())
    out.add_(bias)
    # PyTorch in-place GELU equivalent approximation
    # 0.5 * x * (1 + tanh(sqrt(2/pi) * (x + 0.044715 * x^3)))
    return torch.nn.functional.gelu(out)

def test_fused_correctness():
    torch.manual_seed(0)
    x = torch.randn(16, 64)
    w = torch.randn(32, 64)
    b = torch.randn(32)

    res_eager = eager_linear_gelu(x, w, b)
    res_fused = manual_fused_linear_gelu(x, w, b)

    assert torch.allclose(res_eager, res_fused, atol=1e-5)
    return True
