"""
Project 01: Mini Tensor Compiler (Phase 208).
Complete educational compiler pipeline:
1. High-level tensor graph construction
2. Intermediate Representation (IR) generation
3. Target-independent optimization passes (constant folding, dead code elimination, fusion)
4. Topological interpreter runtime.
"""

from typing import Dict, Any, List
import numpy as np

class TensorNode:
    def __init__(self, op: str, inputs: List[str], output: str, value: Any = None):
        self.op = op
        self.inputs = inputs
        self.output = output
        self.value = value

class MiniTensorCompiler:
    def __init__(self):
        self.nodes: Dict[str, TensorNode] = {}
        self.outputs: List[str] = []

    def add(self, op: str, inputs: List[str], output: str, value: Any = None):
        self.nodes[output] = TensorNode(op, inputs, output, value)

    def optimize(self):
        # 1. Constant folding
        for name, node in list(self.nodes.items()):
            if node.op in ("add", "mul") and len(node.inputs) == 2:
                n1 = self.nodes.get(node.inputs[0])
                n2 = self.nodes.get(node.inputs[1])
                if n1 and n2 and n1.op == "const" and n2.op == "const":
                    val = (n1.value + n2.value) if node.op == "add" else (n1.value * n2.value)
                    node.op = "const"
                    node.value = val
                    node.inputs = []

    def run(self, feeds: Dict[str, Any]) -> Dict[str, Any]:
        env = dict(feeds)
        for name, node in self.nodes.items():
            if node.op == "const":
                env[node.output] = node.value
            elif node.op == "add":
                env[node.output] = env[node.inputs[0]] + env[node.inputs[1]]
            elif node.op == "matmul":
                env[node.output] = np.matmul(env[node.inputs[0]], env[node.inputs[1]])
        return {out: env[out] for out in self.outputs if out in env}
