import os
import sys
import pytest
import numpy as np

sys.path.insert(0, os.path.dirname(__file__))

from mini_graph_runtime import MiniGraph, OpNode, MiniGraphRuntime
from shape_propagation import infer_matmul_shape, infer_elementwise_broadcast, ShapeInferenceError
from tiny_ir import TinyIRModule
from mlir_toy_dialect import MLIRModule

def test_mini_graph_constant_folding():
    g = MiniGraph()
    g.add_node(OpNode("constant", [], "c1", 2.0))
    g.add_node(OpNode("constant", [], "c2", 3.0))
    g.add_node(OpNode("add", ["c1", "c2"], "sum"))
    g.add_node(OpNode("input", [], "x"))
    g.add_node(OpNode("mul", ["sum", "x"], "out"))
    g.set_outputs(["out"])

    folded = g.constant_folding()
    assert folded == 1
    assert g.nodes["sum"].op_type == "constant"
    assert g.nodes["sum"].value == 5.0

    runtime = MiniGraphRuntime(g)
    res = runtime.execute({"x": 10.0})
    assert res["out"] == 50.0

def test_mini_graph_dead_code_elimination():
    g = MiniGraph()
    g.add_node(OpNode("input", [], "x"))
    g.add_node(OpNode("input", [], "dead_in"))
    g.add_node(OpNode("mul", ["dead_in", "dead_in"], "dead_out"))
    g.add_node(OpNode("add", ["x", "x"], "live_out"))
    g.set_outputs(["live_out"])

    removed = g.dead_code_elimination()
    assert removed == 2
    assert "dead_out" not in g.nodes
    assert "dead_in" not in g.nodes
    assert "live_out" in g.nodes

def test_shape_inference():
    # 2D @ 2D
    out_shape = infer_matmul_shape((32, 128), (128, 256))
    assert out_shape == (32, 256)

    # Batched matmul with broadcast
    out_batched = infer_matmul_shape((4, 1, 16, 64), (1, 8, 64, 32))
    assert out_batched == (4, 8, 16, 32)

    # Mismatch
    with pytest.raises(ShapeInferenceError):
        infer_matmul_shape((32, 128), (64, 256))

def test_tiny_ir_pattern_rewriting():
    ir = TinyIRModule()
    x = ir.new_val("f32", (10,))
    one = ir.new_val("f32", ())
    # mul(x, 1.0)
    res = ir.emit("mul", [x, one], attributes={"constant_val": 1.0})
    assert len(ir.instructions) == 1

    rewrites = ir.pattern_rewrite()
    assert rewrites == 1
    assert len(ir.instructions) == 0 # Identity removed

def test_mlir_lowering():
    m = MLIRModule()
    m.add_matmul("c", "a", "b", 16, 64, 32)
    assert len(m.tensor_ops) == 1
    m.lower_tensor_to_loops()
    assert len(m.tensor_ops) == 0
    assert len(m.lowered_loops) == 1
    ir_str = m.print_ir()
    assert "affine.for" in ir_str
