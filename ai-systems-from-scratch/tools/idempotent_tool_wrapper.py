"""
Idempotent Tool Execution Wrapper (Phase 167).
Prevents duplicate external side-effects (e.g., credit card charges, email dispatches)
when an agent loop retries a failed or timed-out tool call.
"""

from typing import Dict, Any, Callable
import time

class IdempotencyStore:
    def __init__(self):
        # Maps idempotency_key -> cached_response
        self._cache: Dict[str, Dict[str, Any]] = {}

    def execute_idempotent(
        self,
        idempotency_key: str,
        tool_fn: Callable[[], Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        If idempotency_key was already processed, returns cached result
        without re-executing tool_fn.
        """
        if idempotency_key in self._cache:
            entry = self._cache[idempotency_key]
            return {
                **entry["result"],
                "_cached_replay": True,
                "_original_timestamp": entry["timestamp"]
            }

        # First execution
        result = tool_fn()
        self._cache[idempotency_key] = {
            "result": result,
            "timestamp": time.time()
        }
        return {
            **result,
            "_cached_replay": False
        }
