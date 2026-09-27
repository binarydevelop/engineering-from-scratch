"""
KV Cache Implementation & Memory Accounting (Phases 10, 55).
Demonstrates:
1. Redundant recomputation in naive autoregressive generation ($O(S^2)$).
2. KV Cache storing past Key/Value projections ($O(S)$ per token).
3. Exact memory formula calculation for KV cache across layers, heads, and context lengths.
"""

from typing import Tuple, Dict
import torch

class SimpleKVCache:
    def __init__(self, num_layers: int, num_heads: int, head_dim: int, max_seq_len: int, dtype: torch.dtype = torch.float32):
        self.num_layers = num_layers
        self.num_heads = num_heads
        self.head_dim = head_dim
        self.max_seq_len = max_seq_len
        self.dtype = dtype
        
        # Preallocated buffers: [layers, 2 (K and V), num_heads, max_seq_len, head_dim]
        self.k_cache = [torch.zeros(num_heads, max_seq_len, head_dim, dtype=dtype) for _ in range(num_layers)]
        self.v_cache = [torch.zeros(num_heads, max_seq_len, head_dim, dtype=dtype) for _ in range(num_layers)]
        self.current_seq_len = 0

    def update(self, layer_idx: int, new_k: torch.Tensor, new_v: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Appends new single-token Key and Value to layer cache:
        new_k, new_v shape: [num_heads, 1, head_dim]
        Returns active history up to current_seq_len.
        """
        pos = self.current_seq_len
        self.k_cache[layer_idx][:, pos:pos+1, :] = new_k
        self.v_cache[layer_idx][:, pos:pos+1, :] = new_v
        return self.k_cache[layer_idx][:, :pos+1, :], self.v_cache[layer_idx][:, :pos+1, :]

    def advance_step(self):
        self.current_seq_len += 1

    @staticmethod
    def calculate_memory_bytes(
        num_layers: int,
        num_heads: int,
        head_dim: int,
        seq_len: int,
        batch_size: int = 1,
        dtype_bytes: int = 2 # 2 for FP16/BF16, 4 for FP32
    ) -> int:
        """
        Exact theoretical formula:
        Memory = 2 (K and V) * num_layers * batch_size * num_heads * seq_len * head_dim * dtype_bytes
        """
        return 2 * num_layers * batch_size * num_heads * seq_len * head_dim * dtype_bytes

def memory_footprint_report(num_layers=32, num_heads=32, head_dim=128, seq_lens=[512, 2048, 8192, 32768], batch_size=1) -> Dict[int, float]:
    """Calculates KV cache footprint in Megabytes across context lengths for typical 7B model."""
    report = {}
    for seq in seq_lens:
        b = SimpleKVCache.calculate_memory_bytes(num_layers, num_heads, head_dim, seq, batch_size, dtype_bytes=2)
        report[seq] = b / (1024 * 1024) # MB
    return report
