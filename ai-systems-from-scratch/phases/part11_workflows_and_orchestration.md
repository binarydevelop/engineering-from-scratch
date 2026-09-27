# Part XI — Workflows & Orchestration (Phases 145 – 154)

> **Motto:** If ordinary procedural code can decide the next step, prefer ordinary code. Agent autonomy must be justified by measurement.

---

## Phases 145 – 149: Determinism, State Machines & Planners
- **Phase 145 — Deterministic Workflow vs Agent:** The autonomy spectrum: when ordinary deterministic code is superior to an LLM.
- **Phase 146 — Workflow State Machine:** Building an explicit Finite State Machine (FSM) where models govern select transitions (`agents/workflow_state_machine.py`).
- **Phase 147 — Semantic Router:** Fast embedding-based or small-model classification routing user queries to bounded handlers.
- **Phase 148 — Planner / Executor Architecture:** Generating an upfront execution plan, sequentially evaluating steps, and replanning.
- **Phase 149 — Loop Limits & Circuit Breakers:** Hard iteration caps, token expenditure limits, and infinite loop detectors.

---

## Phases 150 – 154: Handoffs, Multi-Agent Skepticism & SDKs
- **Phase 150 — Agent Handoffs:** Structured control transfer between specialized agents with explicit state handoff contracts.
- **Phase 151 — Multi-Agent Skepticism:** Debunking "agent swarms"; measuring token bloat and error amplification vs single agent (`experiments/single_vs_multi_agent.py`).
- **Phase 152 — Multi-Agent Communication:** Strict communication protocols: preventing unconstrained agent-to-agent chatter.
- **Phase 153 — Introduce Agent SDK:** Mapping our manual agent loops, tools, and routers to production SDKs.
- **Phase 154 — Framework Escape Hatch:** Deconstructing a framework agent into its manual equivalent to debug production hangs.
