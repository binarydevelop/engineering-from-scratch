"""
Gradient Clipping From Scratch (Phase 78).
Implements L2 norm calculation and adaptive gradient scaling to prevent
exploding gradients from destabilizing training dynamics.
"""

from typing import Iterable
import torch

def clip_grad_norm_scratch(parameters: Iterable[torch.Tensor], max_norm: float) -> float:
    """
    Computes total gradient L2 norm:
    total_norm = sqrt(sum(||g||^2))
    clip_coeff = max_norm / (total_norm + 1e-6)
    if clip_coeff < 1: g = g * clip_coeff
    """
    params = [p for p in parameters if p.grad is not None]
    if not params:
        return 0.0

    total_norm_sq = 0.0
    for p in params:
        param_norm = p.grad.data.norm(2)
        total_norm_sq += param_norm.item() ** 2

    total_norm = total_norm_sq ** 0.5
    clip_coef = max_norm / (total_norm + 1e-6)

    if clip_coef < 1.0:
        for p in params:
            p.grad.data.mul_(clip_coef)

    return total_norm
