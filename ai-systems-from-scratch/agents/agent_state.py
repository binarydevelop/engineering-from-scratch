"""
Agent State Management (Phase 128).
Strict separation of:
1. Message History (prompts and assistant messages sent to LLM)
2. Scratchpad State (agent internal reasoning notes, plan checklist)
3. Application State (external database entities, user preferences)
4. Runtime Execution Counters (turns taken, token consumption, dollars spent)
"""

from typing import List, Dict, Any
from dataclasses import dataclass, field

@dataclass
class AgentState:
    session_id: str
    messages: List[Dict[str, str]] = field(default_factory=list)
    scratchpad: Dict[str, Any] = field(default_factory=dict)
    application_state: Dict[str, Any] = field(default_factory=dict)
    turn_count: int = 0
    total_tokens: int = 0
    budget_spent_usd: float = 0.0
    status: str = "INITIALIZED"

    def record_turn(self, tokens_used: int, cost_usd: float):
        self.turn_count += 1
        self.total_tokens += tokens_used
        self.budget_spent_usd += cost_usd

    def add_message(self, role: str, content: str):
        self.messages.append({"role": role, "content": content})
