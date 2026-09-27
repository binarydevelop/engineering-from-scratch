"""
Shape Propagation & Inference Engine (Phases 23-24).
Symbolic and concrete tensor shape reasoning across matmul, broadcasted add,
and transpositions. Identifies static vs dynamic dimension mismatches.
"""

from typing import Tuple, List, Union

Dim = Union[int, str] # int for concrete shape, str for dynamic symbolic dimension (e.g. 'batch_size')

class ShapeInferenceError(Exception):
    pass

def infer_matmul_shape(shape_a: Tuple[Dim, ...], shape_b: Tuple[Dim, ...]) -> Tuple[Dim, ...]:
    """
    Infers matrix multiplication shape: [..., M, K] x [..., K, N] -> [..., M, N].
    """
    if len(shape_a) < 2 or len(shape_b) < 2:
        raise ShapeInferenceError(f"Matmul requires at least 2D tensors, got {shape_a} and {shape_b}")
    
    k1 = shape_a[-1]
    k2 = shape_b[-2]
    
    # Verify contraction dimension
    if isinstance(k1, int) and isinstance(k2, int) and k1 != k2:
        raise ShapeInferenceError(f"Contraction dimension mismatch: {k1} vs {k2} in {shape_a} @ {shape_b}")
    
    m = shape_a[-2]
    n = shape_b[-1]
    
    # Broadcast batch dimensions
    batch_a = shape_a[:-2]
    batch_b = shape_b[:-2]
    batch_out = []
    
    max_len = max(len(batch_a), len(batch_b))
    padded_a = (1,) * (max_len - len(batch_a)) + batch_a
    padded_b = (1,) * (max_len - len(batch_b)) + batch_b
    
    for d_a, d_b in zip(padded_a, padded_b):
        if d_a == 1:
            batch_out.append(d_b)
        elif d_b == 1:
            batch_out.append(d_a)
        elif d_a == d_b:
            batch_out.append(d_a)
        else:
            raise ShapeInferenceError(f"Cannot broadcast batch dimensions {d_a} and {d_b}")
            
    return tuple(batch_out) + (m, n)

def infer_elementwise_broadcast(shape_a: Tuple[Dim, ...], shape_b: Tuple[Dim, ...]) -> Tuple[Dim, ...]:
    """Infers NumPy-style broadcasted elementwise operation shape."""
    max_len = max(len(shape_a), len(shape_b))
    padded_a = (1,) * (max_len - len(shape_a)) + shape_a
    padded_b = (1,) * (max_len - len(shape_b)) + shape_b
    
    out_shape = []
    for d_a, d_b in zip(padded_a, padded_b):
        if d_a == 1:
            out_shape.append(d_b)
        elif d_b == 1:
            out_shape.append(d_a)
        elif d_a == d_b:
            out_shape.append(d_a)
        elif isinstance(d_a, str) or isinstance(d_b, str):
            out_shape.append(d_a if d_b == 1 else d_b)
        else:
            raise ShapeInferenceError(f"Broadcast failure between {shape_a} and {shape_b}")
    return tuple(out_shape)
