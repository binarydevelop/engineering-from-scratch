# The Production Agent Runtime Architecture

> **Motto:** An agent is not magic. An agent is a deterministic software loop wrapped around a probabilistic next-token generator.

---

## 1. The 12 Mandatory Agent Design Questions

Before creating an agent, you must answer and document these twelve questions:

```text
 1. WHY IS AN AGENT NEEDED?
    Why can ordinary procedural code or a deterministic pipeline not solve this?

 2. COULD DETERMINISTIC CODE SOLVE IT?
    If step order is fixed (A -> B -> C), use a standard Python function, not an LLM agent!

 3. WHAT CHOICES MAY THE MODEL MAKE?
    Is the model choosing a tool? Extracting arguments? Or deciding when a task is finished?

 4. WHICH TOOLS EXIST?
    List every exposed tool with strict parameter types and descriptions.

 5. WHICH ACTIONS MUTATE EXTERNAL STATE?
    Separate read-only tools from state-mutating tools (payments, file writes, DB deletes).

 6. WHAT PERMISSIONS APPLY?
    What authenticated identity is executing the tool? Does the model have least-privilege scope?

 7. WHAT STATE PERSISTS?
    What is preserved across turns: conversation messages, scratchpad notes, or application DB?

 8. WHAT IS THE STOPPING CONDITION?
    How does the runtime know the task has succeeded without depending on model goodwill?

 9. WHAT IS THE MAXIMUM BUDGET?
    What dollar amount ($0.50, $2.00) caps cumulative LLM and tool costs?

10. WHAT IS THE MAXIMUM NUMBER OF TURNS?
    What iteration ceiling (e.g., max 10 iterations) prevents runaway loops?

11. HOW IS SUCCESS EVALUATED?
    What deterministic schema, unit test, or rubric verifies the final outcome?

12. WHAT HAPPENS WHEN A TOOL FAILS?
    Does the agent retry, degrade gracefully, report error to user, or request human intervention?
```

---

## 2. The Core Agent Control Loop

```python
def run_agent_loop(user_query: str, tools: dict, max_turns: int = 10, budget_usd: float = 0.50):
    messages = [{"role": "user", "content": user_query}]
    state = AgentState(budget_spent=0.0, turns=0)
    
    while state.turns < max_turns and state.budget_spent < budget_usd:
        state.turns += 1
        
        # 1. Invoke Model with Tool Schemas
        response = call_model_with_tools(messages, tools=tools.schemas())
        state.budget_spent += response.cost_usd
        messages.append(response.message)
        
        # 2. Check Termination
        if not response.tool_calls:
            return AgentResult(status="SUCCESS", output=response.content, state=state)
            
        # 3. Process Tool Invocations
        for tool_call in response.tool_calls:
            # Defensive validation before execution
            validation_error = tools.validate(tool_call.name, tool_call.arguments)
            if validation_error:
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": f"Schema Validation Error: {validation_error}. Fix arguments."
                })
                continue
                
            # Permission & Approval Check
            if tools.requires_approval(tool_call.name):
                return AgentResult(status="PENDING_APPROVAL", pending_call=tool_call, state=state)
                
            # Safe Execution with Timeout
            tool_result = tools.execute_with_timeout(tool_call.name, tool_call.arguments, timeout_sec=5.0)
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": tool_result
            })
            
    return AgentResult(status="BUDGET_OR_TURN_EXHAUSTED", state=state)
```

---

## 3. The Autonomy Spectrum: When Ordinary Code Wins

```text
Full Determinism                                                         Full Autonomy
[Hardcoded Pipeline] ──► [Deterministic FSM] ──► [Semantic Router] ──► [Autonomous Agent]
(Data ETL, Payments)     (Checkout Flow, Auth)   (FAQ vs Support)      (Exploratory Research)
  - Zero LLM variance      - Strict state gates    - 1 LLM classification- Multi-turn planning
  - 100% reproducible      - Validated branches    - Fast & cheap         - Complex & expensive
```

**Rule of Thumb:** Push as much workflow logic as possible to the left of the spectrum. Use autonomous agent loops only when the branching space cannot be enumerated upfront.
