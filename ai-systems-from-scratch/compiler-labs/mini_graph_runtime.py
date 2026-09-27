"""
Mini Graph Runtime & Optimizer (Phases 13-16).
Builds a Directed Acyclic Graph (DAG) of tensor operations, performs
dead-node elimination, constant folding, and common subexpression elimination (CSE),
and executes via a topological interpreter.
"""

from typing import Dict, List, Any, Set, Tuple, Optional
import numpy as np

class OpNode:
    def __init__(self, op_type: str, inputs: List[str], output_name: str, value: Optional[Any] = None):
        self.op_type = op_type          # 'constant', 'input', 'add', 'mul', 'matmul', 'relu'
        self.inputs = inputs            # List of input node names
        self.output_name = output_name  # Unique name for output value
        self.value = value              # Literal value if constant or input

    def __repr__(self):
        return f"Node({self.output_name} = {self.op_type}({', '.join(self.inputs)}))"

class MiniGraph:
    def __init__(self):
        self.nodes: Dict[str, OpNode] = {}
        self.outputs: List[str] = []

    def add_node(self, node: OpNode):
        self.nodes[node.output_name] = node

    def set_outputs(self, outputs: List[str]):
        self.outputs = outputs

    def get_topological_order(self) -> List[OpNode]:
        """Returns nodes in topological dependency order."""
        visited: Set[str] = set()
        order: List[OpNode] = []

        def dfs(name: str):
            if name in visited:
                return
            visited.add(name)
            node = self.nodes.get(name)
            if node:
                for inp in node.inputs:
                    dfs(inp)
                order.append(node)

        for out in self.outputs:
            dfs(out)
        return order

    def constant_folding(self) -> int:
        """
        Compiler pass: Evaluates constant operations at compile-time.
        Returns the number of folded nodes.
        """
        folded_count = 0
        order = self.get_topological_order()
        for node in order:
            if node.op_type in ("add", "mul") and len(node.inputs) == 2:
                in0 = self.nodes[node.inputs[0]]
                in1 = self.nodes[node.inputs[1]]
                if in0.op_type == "constant" and in1.op_type == "constant":
                    # Evaluate at compile-time
                    if node.op_type == "add":
                        new_val = in0.value + in1.value
                    elif node.op_type == "mul":
                        new_val = in0.value * in1.value
                    
                    node.op_type = "constant"
                    node.value = new_val
                    node.inputs = []
                    folded_count += 1
        return folded_count

    def dead_code_elimination(self) -> int:
        """
        Compiler pass: Removes nodes whose outputs are never read by required outputs.
        Returns the number of removed dead nodes.
        """
        needed: Set[str] = set()
        def mark(name: str):
            if name in needed:
                return
            needed.add(name)
            node = self.nodes.get(name)
            if node:
                for inp in node.inputs:
                    mark(inp)

        for out in self.outputs:
            mark(out)

        dead_keys = [k for k in self.nodes if k not in needed]
        for k in dead_keys:
            del self.nodes[k]
        return len(dead_keys)

    def common_subexpression_elimination(self) -> int:
        """
        Compiler pass: Merges duplicate operations with identical inputs.
        Returns the number of eliminated subexpressions.
        """
        cse_count = 0
        seen_expressions: Dict[Tuple[str, Tuple[str, ...]], str] = {}
        replacement_map: Dict[str, str] = {}

        order = self.get_topological_order()
        for node in order:
            # Update inputs if any predecessor was replaced
            node.inputs = [replacement_map.get(inp, inp) for inp in node.inputs]

            if node.op_type in ("add", "mul", "matmul", "relu"):
                key = (node.op_type, tuple(node.inputs))
                if key in seen_expressions:
                    existing_name = seen_expressions[key]
                    replacement_map[node.output_name] = existing_name
                    cse_count += 1
                else:
                    seen_expressions[key] = node.output_name

        # Apply replacements to outputs and remaining nodes
        self.outputs = [replacement_map.get(out, out) for out in self.outputs]
        # Remove replaced nodes
        for dead_name in replacement_map:
            if dead_name in self.nodes:
                del self.nodes[dead_name]

        return cse_count

class MiniGraphRuntime:
    """Interpreter executing graph nodes in topological sequence."""
    def __init__(self, graph: MiniGraph):
        self.graph = graph

    def execute(self, feed_dict: Dict[str, Any]) -> Dict[str, Any]:
        env: Dict[str, Any] = {}
        # Load feeds
        for k, v in feed_dict.items():
            env[k] = v

        order = self.graph.get_topological_order()
        for node in order:
            if node.op_type == "constant":
                env[node.output_name] = node.value
            elif node.op_type == "input":
                # Already populated from feed_dict
                pass
            elif node.op_type == "add":
                env[node.output_name] = env[node.inputs[0]] + env[node.inputs[1]]
            elif node.op_type == "mul":
                env[node.output_name] = env[node.inputs[0]] * env[node.inputs[1]]
            elif node.op_type == "matmul":
                env[node.output_name] = np.matmul(env[node.inputs[0]], env[node.inputs[1]])
            elif node.op_type == "relu":
                inp = env[node.inputs[0]]
                env[node.output_name] = np.maximum(0, inp)
            else:
                raise ValueError(f"Unknown op type: {node.op_type}")

        return {out: env[out] for out in self.graph.outputs}
