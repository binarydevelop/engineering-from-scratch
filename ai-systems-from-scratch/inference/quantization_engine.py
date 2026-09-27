"""
Quantization From First Principles (Phases 59-64).
Implements:
1. Symmetric & Asymmetric INT8 Quantization (scale & zero-point).
2. Weight-only linear layer quantization.
3. Quantization error evaluation (Mean Squared Error & Cosine Similarity).
4. INT4 packing representation simulation.
"""

from typing import Tuple, Dict
import torch

def quantize_symmetric_int8(tensor: torch.Tensor) -> Tuple[torch.Tensor, float]:
    """
    Symmetric Quantization to [-127, 127]:
    scale = max(abs(tensor)) / 127
    q = round(tensor / scale)
    """
    max_val = torch.max(torch.abs(tensor)).item()
    scale = max_val / 127.0 if max_val > 0 else 1.0
    q_tensor = torch.clamp(torch.round(tensor / scale), -127, 127).to(torch.int8)
    return q_tensor, scale

def dequantize_symmetric_int8(q_tensor: torch.Tensor, scale: float) -> torch.Tensor:
    """Dequantizes INT8 back to FP32: out = q * scale."""
    return q_tensor.to(torch.float32) * scale

def quantize_asymmetric_uint8(tensor: torch.Tensor) -> Tuple[torch.Tensor, float, int]:
    """
    Asymmetric Quantization to [0, 255]:
    scale = (max - min) / 255
    zero_point = round(-min / scale)
    q = clamp(round(tensor / scale) + zero_point, 0, 255)
    """
    min_val = torch.min(tensor).item()
    max_val = torch.max(tensor).item()
    val_range = max_val - min_val
    scale = val_range / 255.0 if val_range > 0 else 1.0
    zero_point = int(round(-min_val / scale))
    zero_point = max(0, min(255, zero_point))

    q_tensor = torch.clamp(torch.round(tensor / scale) + zero_point, 0, 255).to(torch.uint8)
    return q_tensor, scale, zero_point

def dequantize_asymmetric_uint8(q_tensor: torch.Tensor, scale: float, zero_point: int) -> torch.Tensor:
    return (q_tensor.to(torch.float32) - zero_point) * scale

def evaluate_quantization_error(original: torch.Tensor, reconstructed: torch.Tensor) -> Dict[str, float]:
    """Calculates MSE, Peak Signal-to-Noise Ratio (PSNR), and Cosine Similarity."""
    mse = torch.mean((original - reconstructed) ** 2).item()
    norm_orig = torch.norm(original)
    norm_recon = torch.norm(reconstructed)
    cos_sim = (torch.sum(original * reconstructed) / (norm_orig * norm_recon + 1e-8)).item()
    
    return {
        "mse": mse,
        "cosine_similarity": cos_sim,
        "max_absolute_error": torch.max(torch.abs(original - reconstructed)).item()
    }

class QuantizedLinearWeightOnly:
    """Simulates 8-bit weight-only linear layer: weights stored in INT8, activations FP32."""
    def __init__(self, weight_fp32: torch.Tensor):
        self.q_weight, self.scale = quantize_symmetric_int8(weight_fp32)
        self.in_features = weight_fp32.shape[1]
        self.out_features = weight_fp32.shape[0]

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # On-the-fly dequantize or integer GEMM
        w_dequant = dequantize_symmetric_int8(self.q_weight, self.scale)
        return torch.matmul(x, w_dequant.t())
