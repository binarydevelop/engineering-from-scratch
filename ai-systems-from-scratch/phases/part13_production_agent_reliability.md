# Part XIII — Production Agent Reliability (Phases 164 – 174)

> **Motto:** Network connections fail, providers return 429s, and tools timeout. Production reliability requires defensive engineering at every boundary.

---

## Phases 164 – 168: Outages, Timeouts, Retries & Jitter
- **Phase 164 — Model Calls Fail:** Simulating 429 rate limits, 503 service outages, connection timeouts, and empty responses.
- **Phase 165 — Timeouts & Deadlines:** Context-aware request deadlines propagating across nested tool and model invocations.
- **Phase 166 — Safe Retries:** Differentiating idempotent read operations from non-idempotent mutation operations.
- **Phase 167 — Idempotent Tool Execution:** Idempotency keys: preventing double-billing or duplicate emails on network failure (`tools/idempotent_tool_wrapper.py`).
- **Phase 168 — Exponential Backoff & Jitter:** Preventing thundering herd problem during model provider downtime.

---

## Phases 169 – 174: Routing, Caching & Concurrency Control
- **Phase 169 — Fallback Models:** Graceful degradation: switching to secondary model providers when primary is unavailable.
- **Phase 170 — Dynamic Model Routing:** Routing simple queries to cheap models and complex queries to frontier models.
- **Phase 171 — Caching AI Work:** Semantic embedding cache and exact prompt cache; cache invalidation strategies.
- **Phase 172 — Rate Limiting Architecture:** Token bucket and leaky bucket algorithms bounding user and model call rates.
- **Phase 173 — Backpressure & Queueing:** Worker pools bounding concurrent LLM calls to prevent system starvation.
- **Phase 174 — Cooperative Cancellation:** Propagating user cancellation signals to abort in-flight generation and tool execution.
