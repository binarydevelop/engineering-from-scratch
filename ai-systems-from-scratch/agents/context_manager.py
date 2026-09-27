"""
Context Window & Token Budget Management (Phases 129-130).
Treats prompt context as an expensive finite resource. Implements:
1. Token length calculation.
2. Sliding window history truncation (preserving system prompt).
3. Context compaction & summarization simulation.
"""

from typing import List, Dict, Any

class ContextManager:
    def __init__(self, max_context_tokens: int = 4096, reserve_output_tokens: int = 512):
        self.max_context_tokens = max_context_tokens
        self.reserve_output_tokens = reserve_output_tokens
        self.effective_prompt_limit = max_context_tokens - reserve_output_tokens

    @staticmethod
    def estimate_tokens(text: str) -> int:
        """Rough rule of thumb: ~4 characters per token for English."""
        return max(1, len(text) // 4)

    def prune_messages(self, messages: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """
        Preserves index 0 (system prompt).
        Truncates oldest intermediate user/assistant turns if total tokens exceed limit.
        """
        if not messages:
            return []

        system_msg = messages[0] if messages[0].get("role") == "system" else None
        conversation = messages[1:] if system_msg else messages[:]

        current_tokens = sum(self.estimate_tokens(m["content"]) for m in messages)
        if current_tokens <= self.effective_prompt_limit:
            return messages

        # Prune oldest messages from conversation
        while conversation and current_tokens > self.effective_prompt_limit:
            dropped = conversation.pop(0)
            current_tokens -= self.estimate_tokens(dropped["content"])

        if system_msg:
            return [system_msg] + conversation
        return conversation
