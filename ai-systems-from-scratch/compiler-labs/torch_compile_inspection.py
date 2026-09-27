"""
Torch Compile & TorchDynamo Inspector (Phases 26-30).
Demonstrates graph capture, guard generation, graph break detection,
and Inductor compilation in modern PyTorch 2.x.
"""

import torch
import torch._dynamo as dynamo
from typing import List, Dict, Any

class SimpleModule(torch.nn.Module):
    def __init__(self, dim: int = 128):
        super().__init__()
        self.fc1 = torch.nn.Linear(dim, dim)
        self.fc2 = torch.nn.Linear(dim, dim)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        h = torch.relu(self.fc1(x))
        out = self.fc2(h)
        return out

class ModuleWithGraphBreak(torch.nn.Module):
    def __init__(self, dim: int = 64):
        super().__init__()
        self.fc = torch.nn.Linear(dim, dim)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        h = self.fc(x)
        # GRAPH BREAK: Data-dependent Python control flow
        # TorchDynamo cannot trace this purely statically without splitting the graph!
        if h.sum().item() > 0:
            return torch.relu(h)
        else:
            return torch.sigmoid(h)

def inspect_dynamo_graph(model: torch.nn.Module, example_input: torch.Tensor) -> List[Any]:
    """Uses TorchDynamo explanation utility to inspect graph capture and breaks."""
    explanation = dynamo.explain(model, example_input)
    print("--- TorchDynamo Explanation ---")
    print(f"Graph Count: {explanation.graph_count} (If > 1, graph breaks occurred!)")
    print(f"Graph Break Reasons: {explanation.break_reasons}")
    print(f"Ops per graph: {explanation.op_count}")
    return explanation.graphs

if __name__ == "__main__":
    x = torch.randn(8, 128)
    clean_model = SimpleModule(128)
    inspect_dynamo_graph(clean_model, x)
    
    x_break = torch.randn(4, 64)
    break_model = ModuleWithGraphBreak(64)
    inspect_dynamo_graph(break_model, x_break)
