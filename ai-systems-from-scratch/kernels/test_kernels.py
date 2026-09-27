import os
import sys
import pytest
import torch
import numpy as np

sys.path.insert(0, os.path.dirname(__file__))

from cpu_tiled_matmul import naive_matmul, tiled_matmul
from fused_linear_activation import test_fused_correctness as run_fused_check
from numerical_tolerances import compare_precision_loss, verify_kernel_correctness
from triton_kernels import simulate_triton_vector_add, simulate_triton_softmax, run_vector_add

def test_cpu_tiling():
    np.random.seed(0)
    A = np.random.randn(64, 64).astype(np.float32)
    B = np.random.randn(64, 64).astype(np.float32)
    res_naive = naive_matmul(A, B)
    res_tiled = tiled_matmul(A, B, block_size=16)
    np.testing.assert_allclose(res_naive, res_tiled, atol=1e-4)

def test_fused_linear_activation():
    assert run_fused_check() is True

def test_numerical_tolerances():
    # Verify precision loss shows FP32 > BF16/FP16 precision
    res = compare_precision_loss(500)
    assert res["fp32_abs_error"] <= res["fp16_abs_error"] + 1e-5

    # Verify kernel tolerance checker
    x = torch.randn(10, 10, dtype=torch.float32)
    noisy_x = x + 1e-6
    is_close, max_diff, rel_diff = verify_kernel_correctness(noisy_x, x, torch.float32)
    assert is_close is True
    assert max_diff < 1e-5

def test_triton_vector_add_simulation():
    x = torch.randn(250)
    y = torch.randn(250)
    expected = x + y
    simulated = run_vector_add(x, y)
    assert torch.allclose(simulated, expected, atol=1e-5)

def test_triton_softmax_simulation():
    x = torch.randn(4, 32)
    expected = torch.nn.functional.softmax(x, dim=-1)
    simulated = simulate_triton_softmax(x)
    assert torch.allclose(simulated, expected, atol=1e-5)
