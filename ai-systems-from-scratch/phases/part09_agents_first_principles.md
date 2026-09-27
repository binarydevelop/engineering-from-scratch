# Part IX — Agents From First Principles (Phases 121 – 133)

> **Motto:** An agent is not magic. An agent is a deterministic software loop wrapped around a probabilistic next-token generator.

---

## Phases 121 – 127: The Control Loop, Schemas & Tools
- **Phase 121 — Model vs Agent:** The boundary: models predict tokens; agents execute control loops and mutate environment state.
- **Phase 122 — Build Manual Agent Loop:** Writing the pure Python `while not done:` loop without any framework (`agents/manual_agent_loop.py`).
- **Phase 123 — Structured Outputs & Validation:** Enforcing JSON outputs, handling malformed syntax, retrying with error feedback (`agents/structured_output.py`).
- **Phase 124 — Tool Calling Mechanics:** Function calling: extracting tool name, deserializing JSON arguments, calling functions (`agents/tool_dispatcher.py`).
- **Phase 125 — Tool Schema Engineering:** Writing unambiguous, strict schemas (types, constraints, explicit docstrings).
- **Phase 126 — Tool Argument Validation:** Defensive boundary: type casting, range validation, authorization checks.
- **Phase 127 — Tool Error Handling:** Handling tool exceptions, network timeouts, and partial errors gracefully.

---

## Phases 128 – 133: State, Context & Persistent Memory
- **Phase 128 — Agent State Management:** Disentangling conversation messages, working scratchpad, and environment state (`agents/agent_state.py`).
- **Phase 129 — Context Window as a Finite Resource:** Measuring token consumption, degradation of reasoning under long contexts.
- **Phase 130 — Context Management Strategies:** Selection, rolling truncation, recursive summarization, and RAG injection (`agents/context_manager.py`).
- **Phase 131 — Long-Term Memory:** Dissecting model weights vs prompt context vs external persistent key-value memory.
- **Phase 132 — Memory Retrieval:** Semantic search over user memories; measuring false positive memory retrievals.
- **Phase 133 — Memory Updating & Invalidation:** Handling conflicting memories, versioning facts, deleting stale facts (`agents/persistent_memory.py`).
