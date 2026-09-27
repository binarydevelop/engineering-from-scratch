"""
Gradient Accumulation Lab (Phase 76).
Enables training with large effective batch sizes without incurring
prohibitive activation memory by accumulating gradients across micro-batches.
"""

from typing import List
import torch
import torch.nn as nn

def train_with_gradient_accumulation(
    model: nn.Module,
    x: torch.Tensor,
    y: torch.Tensor,
    micro_batch_size: int = 4,
    accumulation_steps: int = 4,
    lr: float = 0.01
) -> List[float]:
    optimizer = torch.optim.SGD(model.parameters(), lr=lr)
    criterion = nn.CrossEntropyLoss()
    optimizer.zero_grad()

    losses = []
    num_samples = len(x)
    total_steps = 0

    for i in range(0, num_samples, micro_batch_size):
        bx = x[i:i+micro_batch_size]
        by = y[i:i+micro_batch_size]

        logits = model(bx)
        # Scale loss by accumulation steps so gradients match true batch mean
        loss = criterion(logits, by) / accumulation_steps
        loss.backward()

        total_steps += 1
        losses.append(loss.item() * accumulation_steps)

        # Step only after accumulating full batch
        if total_steps % accumulation_steps == 0 or (i + micro_batch_size >= num_samples):
            optimizer.step()
            optimizer.zero_grad()

    return losses
