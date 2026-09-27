"""
Custom Optimizers From Scratch (Phase 74).
Implements:
1. Custom SGD with Momentum.
2. Custom AdamW (first/second moments, bias correction, decoupled weight decay).
Reveals exact optimizer state memory overhead (2x model parameter bytes for AdamW).
"""

from typing import List, Dict
import math
import torch

class CustomSGD:
    def __init__(self, params: List[torch.Tensor], lr: float = 0.01, momentum: float = 0.9):
        self.params = [p for p in params if p.requires_grad]
        self.lr = lr
        self.momentum = momentum
        # Velocity state: 1x parameter count
        self.velocities = [torch.zeros_like(p.data) for p in self.params]

    def step(self):
        with torch.no_grad():
            for p, v in zip(self.params, self.velocities):
                if p.grad is None:
                    continue
                v.mul_(self.momentum).add_(p.grad.data)
                p.data.add_(v, alpha=-self.lr)

    def zero_grad(self):
        for p in self.params:
            if p.grad is not None:
                p.grad.detach_()
                p.grad.zero_()

class CustomAdamW:
    def __init__(
        self,
        params: List[torch.Tensor],
        lr: float = 1e-3,
        betas: tuple = (0.9, 0.999),
        eps: float = 1e-8,
        weight_decay: float = 0.01
    ):
        self.params = [p for p in params if p.requires_grad]
        self.lr = lr
        self.beta1, self.beta2 = betas
        self.eps = eps
        self.weight_decay = weight_decay
        self.step_count = 0
        
        # State: m (first moment) and v (second moment) -> 2x parameter memory!
        self.m = [torch.zeros_like(p.data) for p in self.params]
        self.v = [torch.zeros_like(p.data) for p in self.params]

    def step(self):
        self.step_count += 1
        with torch.no_grad():
            for p, m, v in zip(self.params, self.m, self.v):
                if p.grad is None:
                    continue
                grad = p.grad.data
                
                # Decoupled weight decay
                p.data.mul_(1.0 - self.lr * self.weight_decay)

                # Update biased 1st and 2nd moments
                m.mul_(self.beta1).add_(grad, alpha=1.0 - self.beta1)
                v.mul_(self.beta2).addcmul_(grad, grad, value=1.0 - self.beta2)

                # Bias correction terms
                bias_correction1 = 1.0 - self.beta1 ** self.step_count
                bias_correction2 = 1.0 - self.beta2 ** self.step_count

                step_size = self.lr / bias_correction1
                denom = (v.sqrt() / math.sqrt(bias_correction2)).add_(self.eps)

                p.data.addcdiv_(m, denom, value=-step_size)

    def zero_grad(self):
        for p in self.params:
            if p.grad is not None:
                p.grad.detach_()
                p.grad.zero_()
