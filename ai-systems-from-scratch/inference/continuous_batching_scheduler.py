"""
Continuous Batching Scheduler Simulator (Phases 53-54).
Simulates iteration-level scheduling where requests dynamically join
and exit the active generation batch token-by-token, demonstrating
how continuous batching eliminates static batching padding bubbles.
"""

from typing import List, Dict, Optional
import time

class InferenceRequest:
    def __init__(self, req_id: str, prompt_len: int, target_output_len: int, arrival_step: int):
        self.req_id = req_id
        self.prompt_len = prompt_len
        self.target_output_len = target_output_len
        self.arrival_step = arrival_step
        self.generated_tokens = 0
        self.finish_step: Optional[int] = None
        self.first_token_step: Optional[int] = None

    @property
    def is_finished(self) -> bool:
        return self.generated_tokens >= self.target_output_len

class ContinuousBatchingSimulator:
    def __init__(self, max_batch_size: int = 4):
        self.max_batch_size = max_batch_size
        self.waiting_queue: List[InferenceRequest] = []
        self.running_batch: List[InferenceRequest] = []
        self.completed: List[InferenceRequest] = []
        self.current_step = 0
        self.total_tokens_computed = 0

    def add_request(self, req: InferenceRequest):
        self.waiting_queue.append(req)

    def step(self):
        """Simulates one iteration (token generation step) on the GPU."""
        self.current_step += 1

        # 1. Admit new requests up to max_batch_size
        while len(self.running_batch) < self.max_batch_size and self.waiting_queue:
            next_req = self.waiting_queue.pop(0)
            # Prefill: first step marks TTFT
            next_req.first_token_step = self.current_step
            self.running_batch.append(next_req)
            self.total_tokens_computed += next_req.prompt_len

        # 2. Decode step: Generate 1 token for each running request
        still_running = []
        for req in self.running_batch:
            req.generated_tokens += 1
            self.total_tokens_computed += 1
            if req.is_finished:
                req.finish_step = self.current_step
                self.completed.append(req)
            else:
                still_running.append(req)

        self.running_batch = still_running

    def run_until_complete(self) -> Dict[str, float]:
        while self.waiting_queue or self.running_batch:
            self.step()

        latencies = [r.finish_step - r.arrival_step for r in self.completed]
        ttfts = [r.first_token_step - r.arrival_step for r in self.completed]
        total_gen_tokens = sum(r.generated_tokens for r in self.completed)

        return {
            "total_steps": self.current_step,
            "avg_latency_steps": sum(latencies) / len(latencies) if latencies else 0,
            "avg_ttft_steps": sum(ttfts) / len(ttfts) if ttfts else 0,
            "throughput_tokens_per_step": total_gen_tokens / self.current_step if self.current_step > 0 else 0
        }

def simulate_static_batching(requests: List[InferenceRequest], batch_size: int = 4) -> Dict[str, float]:
    """Simulates static batching: batch waits for longest request before admitting next."""
    total_steps = 0
    all_completed = []
    
    for i in range(0, len(requests), batch_size):
        batch = requests[i:i+batch_size]
        max_output = max(r.target_output_len for r in batch)
        # All requests in batch forced to wait max_output steps
        total_steps += max_output
        for r in batch:
            r.finish_step = total_steps
            all_completed.append(r)
            
    total_gen_tokens = sum(r.target_output_len for r in all_completed)
    return {
        "total_steps": total_steps,
        "throughput_tokens_per_step": total_gen_tokens / total_steps if total_steps > 0 else 0
    }
