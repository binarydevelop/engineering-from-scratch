"""
Autograd Graph Debugger (Phase 73).
Inspects dynamic backward graph, grad_fn pointers, identifies detached tensors,
and diagnoses common gradient leakage bugs.
"""

from typing import List, Dict, Any, Optional
import torch

def trace_backward_graph(root_tensor: torch.Tensor) -> List[str]:
    """Traverses backward DAG from loss tensor through grad_fn attributes."""
    visited = set()
    history = []

    def traverse(fn: Optional[Any], depth: int = 0):
        if fn is None or id(fn) in visited:
            return
        visited.add(id(fn))
        name = fn.__class__.__name__
        history.append(f"{'  ' * depth}<- {name}")
        if hasattr(fn, "next_functions"):
            for next_fn, _ in fn.next_functions:
                traverse(next_fn, depth + 1)

    traverse(root_tensor.grad_fn)
    return history

def demonstrate_gradient_block_bug():
    """
    Shows how calling `.detach()` or wrapping in `.item()`
    accidentally severs the computation graph, rendering requires_grad False.
    """
    w = torch.tensor([2.0], requires_grad=True)
    x = torch.tensor([3.0])
    
    # Broken pipeline: .detach() cuts gradient flow
    h = (w * x).detach()
    loss = (h - 10.0) ** 2
    
    # loss.requires_grad is False because graph was severed!
    return loss.requires_grad is False
