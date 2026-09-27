"""
Manual Agent Loop From Scratch (Phase 122).
No LangChain. No CrewAI. No Agent SDKs.
A pure Python while loop wrapped around model decisions, schema validation,
tool dispatching, and circuit breakers (max turns & cost limits).
"""

import os
import sys
from typing import Dict, Any, Callable, List, Optional
import json
from dataclasses import dataclass

sys.path.insert(0, os.path.dirname(__file__))

from agent_state import AgentState
from structured_output import ToolCallRequest, parse_and_validate
from tool_dispatcher import ToolDispatcher

@dataclass
class AgentRunResult:
    status: str
    final_output: Optional[str]
    total_turns: int
    total_cost: float
    history: List[Dict[str, str]]

def run_pure_agent_loop(
    user_query: str,
    dispatcher: ToolDispatcher,
    mock_model_fn: Callable[[List[Dict[str, str]]], str],
    max_turns: int = 5,
    max_budget_usd: float = 0.50
) -> AgentRunResult:
    state = AgentState(session_id="session_001")
    state.add_message("system", "You are an AI assistant. You can invoke tools using JSON: {\"tool_name\": \"...\", \"arguments\": {...}} or reply in plain text.")
    state.add_message("user", user_query)

    cost_per_turn = 0.01 # Simulated turn cost

    while state.turn_count < max_turns and state.budget_spent_usd < max_budget_usd:
        state.record_turn(tokens_used=150, cost_usd=cost_per_turn)

        # 1. Model Call
        raw_response = mock_model_fn(state.messages)
        state.add_message("assistant", raw_response)

        # 2. Check if model requested a tool
        tool_req, parse_err = parse_and_validate(raw_response, ToolCallRequest)
        
        if tool_req:
            # Model emitted structured tool call request
            tool_name = tool_req.tool_name
            tool_args = tool_req.arguments

            # 3. Dispatch Tool
            exec_result = dispatcher.execute(tool_name, tool_args)
            if exec_result["success"]:
                content_str = json.dumps(exec_result["result"])
            else:
                content_str = f"Error: {exec_result['error']}"

            # 4. Feed Observation back to Model
            state.add_message("tool", f"Tool '{tool_name}' returned: {content_str}")

        else:
            # Model replied with final conversational response
            return AgentRunResult(
                status="SUCCESS",
                final_output=raw_response,
                total_turns=state.turn_count,
                total_cost=state.budget_spent_usd,
                history=state.messages
            )

    return AgentRunResult(
        status="EXHAUSTED_TURNS_OR_BUDGET",
        final_output=None,
        total_turns=state.turn_count,
        total_cost=state.budget_spent_usd,
        history=state.messages
    )
