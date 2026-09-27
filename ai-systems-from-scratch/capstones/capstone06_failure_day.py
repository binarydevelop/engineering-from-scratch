"""
Capstone 06: Failure Day (Chaos Engineering for AI Systems) (Phase 228).
Systematic fault injection harness simulating 12 production failure modes:
1. Model timeout
2. Provider 429 rate limit
3. Retrieval service down
4. Vector index stale
5. Tool 500 error
6. Tool timeout
7. Duplicate tool execution (double click)
8. Prompt injection attempt
9. Malformed tool arguments
10. Context window overflow
11. GPU out-of-memory (OOM)
12. Queue overload / backpressure exhaustion
"""

from typing import Dict, Any, List

CHAOS_FAILURES = [
    ("model_timeout", "LLM upstream connection timed out after 5000ms"),
    ("provider_429", "Upstream API returned HTTP 429 Too Many Requests"),
    ("retrieval_down", "Vector index endpoint returned connection refused"),
    ("index_stale", "Retrieved document timestamp is older than policy update"),
    ("tool_500", "Payment gateway tool returned Internal Server Error 500"),
    ("tool_timeout", "Database query exceeded 3000ms execution deadline"),
    ("duplicate_execution", "Client submitted identical request token simultaneously"),
    ("prompt_injection", "User query contained malicious override instruction"),
    ("malformed_args", "Model produced JSON with missing required fields"),
    ("context_overflow", "Accumulated conversation tokens exceeded model max context"),
    ("gpu_oom", "CUDA out of memory during batch prefill allocation"),
    ("queue_overload", "Server queue exceeded 500 pending requests capacity"),
]

def simulate_chaos_injection(failure_type: str) -> Dict[str, Any]:
    matched = [f for f in CHAOS_FAILURES if f[0] == failure_type]
    if not matched:
        return {"injected": False, "status": "UNKNOWN_FAULT"}

    code, desc = matched[0]
    # Simulate graceful fallback / circuit breaker response
    return {
        "injected": True,
        "fault_code": code,
        "description": desc,
        "circuit_breaker_triggered": True,
        "fallback_recovery": f"Graceful fallback applied for {code}."
    }

def run_failure_day_drill() -> Dict[str, Any]:
    results = {}
    for code, _ in CHAOS_FAILURES:
        results[code] = simulate_chaos_injection(code)
    return results

if __name__ == "__main__":
    report = run_failure_day_drill()
    print("Chaos Engineering Failure Day Report (12 Injected Faults):")
    for k, v in report.items():
        print(f"  [{k:20s}] -> Injected: {v['injected']}, Fallback: {v['fallback_recovery']}")
