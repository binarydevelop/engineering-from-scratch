"""
Project 04: Mini Inference Scheduler (Phase 211).
High-performance iteration-level continuous batching scheduler:
- Priority queue for arriving requests
- Dynamic admission control based on memory availability
- Interleaved prefill and decode scheduling
- Paged KV cache block assignment
"""

from typing import List, Dict, Any, Optional

class ScheduledRequest:
    def __init__(self, id_str: str, prompt_len: int, max_tokens: int, priority: int = 1):
        self.id_str = id_str
        self.prompt_len = prompt_len
        self.max_tokens = max_tokens
        self.priority = priority
        self.current_tokens = 0
        self.is_prefilled = False

    @property
    def is_done(self) -> bool:
        return self.current_tokens >= self.max_tokens

class MiniInferenceScheduler:
    def __init__(self, max_batch_slots: int = 4, max_blocks: int = 32):
        self.max_slots = max_batch_slots
        self.max_blocks = max_blocks
        self.available_blocks = max_blocks
        self.waiting: List[ScheduledRequest] = []
        self.active: List[ScheduledRequest] = []
        self.finished: List[ScheduledRequest] = []

    def submit(self, req: ScheduledRequest):
        self.waiting.append(req)
        # Sort by priority descending
        self.waiting.sort(key=lambda r: r.priority, reverse=True)

    def step(self) -> Dict[str, Any]:
        # 1. Admit new requests if slots and memory exist
        while len(self.active) < self.max_slots and self.waiting:
            candidate = self.waiting[0]
            blocks_needed = (candidate.prompt_len + 15) // 16
            if self.available_blocks >= blocks_needed:
                self.waiting.pop(0)
                self.available_blocks -= blocks_needed
                candidate.is_prefilled = True
                self.active.append(candidate)
            else:
                break # Memory constrained

        # 2. Decode iteration: generate 1 token for each active request
        remaining = []
        for req in self.active:
            req.current_tokens += 1
            if req.is_done:
                self.finished.append(req)
                # Release memory blocks
                blocks_used = (req.prompt_len + req.current_tokens + 15) // 16
                self.available_blocks += blocks_used
            else:
                remaining.append(req)

        self.active = remaining
        return {
            "active_count": len(self.active),
            "waiting_count": len(self.waiting),
            "finished_count": len(self.finished),
            "available_blocks": self.available_blocks
        }
