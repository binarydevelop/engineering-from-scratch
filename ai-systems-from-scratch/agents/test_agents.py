import os
import sys
import pytest
from pydantic import BaseModel

sys.path.insert(0, os.path.dirname(__file__))

from structured_output import ToolCallRequest, parse_and_validate, extract_json_block
from agent_state import AgentState
from tool_dispatcher import ToolDispatcher
from context_manager import ContextManager
from persistent_memory import PersistentMemoryStore
from manual_agent_loop import run_pure_agent_loop
from workflow_state_machine import OrderStateMachine, OrderState, SemanticRouter

def test_structured_output():
    raw_text = 'Sure! Here is the tool call:\n```json\n{"tool_name": "calc", "arguments": {"expr": "2+2"}}\n```'
    parsed, err = parse_and_validate(raw_text, ToolCallRequest)
    assert err is None
    assert parsed.tool_name == "calc"
    assert parsed.arguments["expr"] == "2+2"

def test_tool_dispatcher():
    dispatcher = ToolDispatcher()
    dispatcher.register("multiply", lambda a, b: a * b, "Multiplies two numbers", {})
    res = dispatcher.execute("multiply", {"a": 6, "b": 7})
    assert res["success"] is True
    assert res["result"] == 42

def test_context_manager_pruning():
    mgr = ContextManager(max_context_tokens=50, reserve_output_tokens=10) # 40 tokens max prompt
    messages = [
        {"role": "system", "content": "You are a helpful bot."}, # preserved
        {"role": "user", "content": "A" * 80}, # ~20 tokens
        {"role": "assistant", "content": "B" * 80}, # ~20 tokens
        {"role": "user", "content": "C" * 80}, # ~20 tokens (exceeds limit!)
    ]
    pruned = mgr.prune_messages(messages)
    assert pruned[0]["role"] == "system"
    assert len(pruned) < len(messages)

def test_persistent_memory():
    store = PersistentMemoryStore()
    f1 = store.set_fact("user_1", "favorite_color", "blue")
    assert f1.version == 1
    
    # Update fact
    f2 = store.set_fact("user_1", "favorite_color", "green")
    assert f2.version == 2
    
    active = store.get_active_facts("user_1")
    assert active["favorite_color"] == "green"

def test_manual_agent_loop():
    dispatcher = ToolDispatcher()
    dispatcher.register("get_price", lambda item: 29.99 if item == "book" else 0.0, "Get price", {})

    # Mock model: turn 1 requests tool, turn 2 responds with final answer
    call_step = 0
    def mock_model(messages):
        nonlocal call_step
        call_step += 1
        if call_step == 1:
            return '```json\n{"tool_name": "get_price", "arguments": {"item": "book"}}\n```'
        else:
            return "The book costs $29.99."

    res = run_pure_agent_loop("What is the price of book?", dispatcher, mock_model, max_turns=5)
    assert res.status == "SUCCESS"
    assert "29.99" in res.final_output
    assert res.total_turns == 2

def test_workflow_state_machine_and_router():
    fsm = OrderStateMachine()
    assert fsm.state == OrderState.COLLECT_ITEMS
    fsm.transition("add_items", {"items": ["item1"]})
    assert fsm.state == OrderState.VALIDATE_INVENTORY
    fsm.transition("inventory_ok", {})
    assert fsm.state == OrderState.PROCESS_PAYMENT

    router = SemanticRouter()
    assert router.route("I need a refund on my credit card") == "billing"
    assert router.route("There is a 500 error on the page") == "technical_support"
