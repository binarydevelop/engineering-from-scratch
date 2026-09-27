"""
Manual Training Loop From Scratch (Phase 71).
Zero trainer frameworks. Pure PyTorch primitives:
batch -> forward -> loss -> backward -> optimizer.step -> optimizer.zero_grad.
"""

from typing import List, Tuple
import torch
import torch.nn as nn

class TinyMLP(nn.Module):
    def __init__(self, in_features: int = 8, hidden_features: int = 16, out_features: int = 2):
        super().__init__()
        self.fc1 = nn.Linear(in_features, hidden_features)
        self.fc2 = nn.Linear(hidden_features, out_features)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.fc2(torch.relu(self.fc1(x)))

def run_manual_training_loop(epochs: int = 5, lr: float = 0.05) -> List[float]:
    torch.manual_seed(42)
    model = TinyMLP()
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.SGD(model.parameters(), lr=lr)

    # Synthetic dataset: 40 samples
    x = torch.randn(40, 8)
    y = torch.randint(0, 2, (40,))

    loss_history = []
    batch_size = 8

    for epoch in range(epochs):
        epoch_loss = 0.0
        num_batches = 0
        for i in range(0, len(x), batch_size):
            batch_x = x[i:i+batch_size]
            batch_y = y[i:i+batch_size]

            # 1. Forward
            logits = model(batch_x)
            loss = criterion(logits, batch_y)

            # 2. Backward
            loss.backward()

            # 3. Optimizer Step
            optimizer.step()

            # 4. Zero Grad (Critical: omitting this causes gradient accumulation!)
            optimizer.zero_grad()

            epoch_loss += loss.item()
            num_batches += 1

        avg_loss = epoch_loss / num_batches
        loss_history.append(avg_loss)

    return loss_history
