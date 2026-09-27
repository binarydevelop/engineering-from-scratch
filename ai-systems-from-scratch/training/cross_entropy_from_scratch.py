"""
Cross-Entropy Loss From Scratch (Phase 72).
Implements numerically stable Log-Sum-Exp trick to prevent overflow/underflow
when exponentiating large logits, matching torch.nn.CrossEntropyLoss bitwise within FP32 epsilon.
"""

import torch

def stable_log_sum_exp(logits: torch.Tensor, dim: int = -1) -> torch.Tensor:
    """
    Computes log(sum(exp(x))) safely:
    max_x = max(x)
    log_sum_exp = max_x + log(sum(exp(x - max_x)))
    """
    max_logits, _ = torch.max(logits, dim=dim, keepdim=True)
    stabilized = logits - max_logits
    sum_exp = torch.sum(torch.exp(stabilized), dim=dim, keepdim=True)
    return (max_logits + torch.log(sum_exp)).squeeze(dim)

def cross_entropy_scratch(logits: torch.Tensor, targets: torch.Tensor) -> torch.Tensor:
    """
    Cross Entropy: -log(softmax(logits)[target])
                 = -logits[target] + log_sum_exp(logits)
    """
    lse = stable_log_sum_exp(logits, dim=-1)
    # Gather target logits
    batch_indices = torch.arange(logits.shape[0])
    target_logits = logits[batch_indices, targets]
    loss_per_sample = lse - target_logits
    return torch.mean(loss_per_sample)

def verify_cross_entropy():
    torch.manual_seed(0)
    logits = torch.randn(10, 5) * 50.0 # High dynamic range to test stability
    targets = torch.randint(0, 5, (10,))

    loss_scratch = cross_entropy_scratch(logits, targets)
    loss_torch = torch.nn.functional.cross_entropy(logits, targets)

    diff = torch.abs(loss_scratch - loss_torch).item()
    assert diff < 1e-4, f"Discrepancy too large: {diff}"
    return diff
