"""
CPU Tiled Matrix Multiplication (Phase 41).
Demonstrates cache-friendly sub-block tiling (L1/L2 cache locality)
compared to naive triple-loop matrix multiplication.
"""

import time
import numpy as np

def naive_matmul(A: np.ndarray, B: np.ndarray) -> np.ndarray:
    """Naive triple loop O(N^3) with poor spatial/temporal cache locality."""
    M, K = A.shape
    K2, N = B.shape
    assert K == K2
    C = np.zeros((M, N), dtype=A.dtype)
    for i in range(M):
        for j in range(N):
            acc = 0.0
            for k in range(K):
                acc += A[i, k] * B[k, j]
            C[i, j] = acc
    return C

def tiled_matmul(A: np.ndarray, B: np.ndarray, block_size: int = 32) -> np.ndarray:
    """
    Tiled Matrix Multiplication:
    Partitions matrices into sub-blocks of size (block_size x block_size)
    such that active working blocks fit entirely within CPU L1/L2 cache,
    minimizing cache line evictions.
    """
    M, K = A.shape
    K2, N = B.shape
    assert K == K2
    C = np.zeros((M, N), dtype=A.dtype)

    for i0 in range(0, M, block_size):
        i_max = min(i0 + block_size, M)
        for j0 in range(0, N, block_size):
            j_max = min(j0 + block_size, N)
            for k0 in range(0, K, block_size):
                k_max = min(k0 + block_size, K)
                # Sub-block multiplication in cache
                for i in range(i0, i_max):
                    for k in range(k0, k_max):
                        a_ik = A[i, k]
                        for j in range(j0, j_max):
                            C[i, j] += a_ik * B[k, j]
    return C

def benchmark_tiling():
    size = 128 # Kept reasonable for pure Python loop comparison
    np.random.seed(42)
    A = np.random.randn(size, size).astype(np.float32)
    B = np.random.randn(size, size).astype(np.float32)

    t0 = time.perf_counter()
    res_naive = naive_matmul(A, B)
    t_naive = time.perf_counter() - t0

    t0 = time.perf_counter()
    res_tiled = tiled_matmul(A, B, block_size=32)
    t_tiled = time.perf_counter() - t0

    # Verification
    np.testing.assert_allclose(res_naive, res_tiled, atol=1e-4)

    return {
        "naive_sec": t_naive,
        "tiled_sec": t_tiled,
        "speedup": t_naive / t_tiled if t_tiled > 0 else 1.0
    }

if __name__ == "__main__":
    out = benchmark_tiling()
    print("Tiling benchmark:", out)
