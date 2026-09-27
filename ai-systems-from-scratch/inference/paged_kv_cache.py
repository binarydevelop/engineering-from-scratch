"""
Paged KV Cache Block Allocator Simulator (Phases 56-57).
Implements virtual-to-physical block mapping (PagedAttention concept)
demonstrating how non-contiguous fixed-size physical blocks eliminate
both internal and external memory fragmentation.
"""

from typing import List, Dict, Optional
import math

class PhysicalBlock:
    def __init__(self, block_id: int, block_size: int = 16):
        self.block_id = block_id
        self.block_size = block_size
        self.num_tokens = 0
        self.ref_count = 0

    def is_full(self) -> bool:
        return self.num_tokens >= self.block_size

    def append_token(self):
        assert not self.is_full()
        self.num_tokens += 1

class BlockTable:
    """Virtual sequence mapping to physical memory block IDs."""
    def __init__(self, seq_id: str):
        self.seq_id = seq_id
        self.physical_block_ids: List[int] = []

class PagedKVCacheManager:
    def __init__(self, total_blocks: int = 128, block_size: int = 16):
        self.block_size = block_size
        self.total_blocks = total_blocks
        self.free_blocks: List[int] = list(range(total_blocks))
        self.allocated_blocks: Dict[int, PhysicalBlock] = {
            i: PhysicalBlock(i, block_size) for i in range(total_blocks)
        }
        self.block_tables: Dict[str, BlockTable] = {}

    def allocate_sequence(self, seq_id: str, prompt_len: int) -> bool:
        blocks_needed = math.ceil(prompt_len / self.block_size)
        if len(self.free_blocks) < blocks_needed:
            return False # Out of Memory / Insufficient cache blocks

        table = BlockTable(seq_id)
        tokens_remaining = prompt_len
        for _ in range(blocks_needed):
            block_id = self.free_blocks.pop(0)
            block = self.allocated_blocks[block_id]
            block.ref_count = 1
            allocated_tokens = min(tokens_remaining, self.block_size)
            block.num_tokens = allocated_tokens
            tokens_remaining -= allocated_tokens
            table.physical_block_ids.append(block_id)

        self.block_tables[seq_id] = table
        return True

    def append_token(self, seq_id: str) -> bool:
        """Appends 1 token to an active sequence during decode phase."""
        table = self.block_tables[seq_id]
        last_block_id = table.physical_block_ids[-1]
        last_block = self.allocated_blocks[last_block_id]

        if not last_block.is_full():
            last_block.append_token()
            return True

        # Need new physical block
        if not self.free_blocks:
            return False # Cache full!
        new_block_id = self.free_blocks.pop(0)
        new_block = self.allocated_blocks[new_block_id]
        new_block.ref_count = 1
        new_block.num_tokens = 1
        table.physical_block_ids.append(new_block_id)
        return True

    def free_sequence(self, seq_id: str):
        if seq_id not in self.block_tables:
            return
        table = self.block_tables.pop(seq_id)
        for block_id in table.physical_block_ids:
            block = self.allocated_blocks[block_id]
            block.ref_count -= 1
            if block.ref_count == 0:
                block.num_tokens = 0
                self.free_blocks.append(block_id)

    def memory_utilization(self) -> float:
        """Calculates actual token capacity utilized vs allocated blocks."""
        used_blocks = self.total_blocks - len(self.free_blocks)
        if used_blocks == 0:
            return 1.0
        active_tokens = sum(
            self.allocated_blocks[b].num_tokens for b in range(self.total_blocks)
            if self.allocated_blocks[b].ref_count > 0
        )
        total_allocated_capacity = used_blocks * self.block_size
        return active_tokens / total_allocated_capacity
