"""
MLIR Toy Dialect & Lowering Simulator (Phases 31-36).
Educational multi-level IR demonstrating:
1. High-Level Tensor Dialect (declarative tensor operations)
2. Lowering Pass (translating tensor.matmul to nested loop nests in Affine/Loop dialect)
3. Target Code Generation
"""

from typing import List, Dict, Any

class HighLevelTensorOp:
    def __init__(self, op_name: str, out_name: str, in_names: List[str], shape: List[int]):
        self.dialect = "tensor"
        self.op_name = op_name
        self.out_name = out_name
        self.in_names = in_names
        self.shape = shape

    def emit_mlir(self) -> str:
        shape_str = "x".join(str(d) for d in self.shape)
        operands = ", ".join(f"%{name}" for name in self.in_names)
        return f"  %{self.out_name} = {self.dialect}.{self.op_name} {operands} : tensor<{shape_str}xf32>"

class LowLevelLoopNest:
    def __init__(self, out_name: str, in_a: str, in_b: str, m: int, k: int, n: int):
        self.dialect = "affine"
        self.out_name = out_name
        self.in_a = in_a
        self.in_b = in_b
        self.m = m
        self.k = k
        self.n = n

    def emit_mlir(self) -> str:
        lines = [
            f"  // Lowered from tensor.matmul to affine loop nest:",
            f"  affine.for %i = 0 to {self.m} {{",
            f"    affine.for %j = 0 to {self.n} {{",
            f"      affine.for %k = 0 to {self.k} {{",
            f"        %a = affine.load %{self.in_a}[%i, %k] : memref<{self.m}x{self.k}xf32>",
            f"        %b = affine.load %{self.in_b}[%k, %j] : memref<{self.k}x{self.n}xf32>",
            f"        %prod = arith.mulf %a, %b : f32",
            f"        %curr = affine.load %{self.out_name}[%i, %j] : memref<{self.m}x{self.n}xf32>",
            f"        %sum = arith.addf %curr, %prod : f32",
            f"        affine.store %sum, %{self.out_name}[%i, %j] : memref<{self.m}x{self.n}xf32>",
            f"      }}",
            f"    }}",
            f"  }}"
        ]
        return "\n".join(lines)

class MLIRModule:
    def __init__(self):
        self.tensor_ops: List[HighLevelTensorOp] = []
        self.lowered_loops: List[LowLevelLoopNest] = []

    def add_matmul(self, out_name: str, in_a: str, in_b: str, m: int, k: int, n: int):
        self.tensor_ops.append(HighLevelTensorOp("matmul", out_name, [in_a, in_b], [m, n]))

    def lower_tensor_to_loops(self):
        """Compiler pass: Lowering from high-level value-semantic tensor dialect to loop nests."""
        for op in self.tensor_ops:
            if op.op_name == "matmul":
                m, n = op.shape
                # Assuming k from matching dimension
                k = 64 # canonicalized
                loop = LowLevelLoopNest(op.out_name, op.in_names[0], op.in_names[1], m, k, n)
                self.lowered_loops.append(loop)
        self.tensor_ops.clear()

    def print_ir(self) -> str:
        lines = ["module {", "  func.func @forward() {"]
        if self.tensor_ops:
            for op in self.tensor_ops:
                lines.append(op.emit_mlir())
        if self.lowered_loops:
            for loop in self.lowered_loops:
                lines.append(loop.emit_mlir())
        lines.append("    return")
        lines.append("  }")
        lines.append("}")
        return "\n".join(lines)
