#!/usr/bin/env bash
# Failure Injection Dispatcher Script
# Executes controlled failures adhering to SAFETY.md

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

SCENARIO="${1:-help}"

case "$SCENARIO" in
    payment-latency)
        DELAY_MS="${2:-1200}"
        echo "[CHAOS] Injecting ${DELAY_MS}ms artificial latency into payment-service..."
        python3 "${REPO_ROOT}/chaos/latency_injector.py" --service payment-service --delay-ms "${DELAY_MS}"
        ;;
    payment-failure)
        RATE="${2:-0.40}"
        echo "[CHAOS] Injecting ${RATE} error rate into payment-service..."
        python3 "${REPO_ROOT}/chaos/latency_injector.py" --service payment-service --error-rate "${RATE}"
        ;;
    db-pool-exhaust)
        CONNS="${2:-55}"
        echo "[CHAOS] Exhausting PostgreSQL connection pool with ${CONNS} idle transactions..."
        python3 "${REPO_ROOT}/chaos/db_connection_exhaust.py" --connections "${CONNS}"
        ;;
    cpu-burn)
        DURATION="${2:-30}"
        echo "[CHAOS] Burning 100% CPU on target worker for ${DURATION}s..."
        python3 "${REPO_ROOT}/chaos/cpu_burn.py" --duration "${DURATION}"
        ;;
    memory-leak)
        RATE_MB="${2:-50}"
        echo "[CHAOS] Simulating memory leak at ${RATE_MB} MB/s..."
        python3 "${REPO_ROOT}/chaos/memory_leak.py" --rate-mb "${RATE_MB}"
        ;;
    reset)
        echo "[CHAOS] Resetting all injected failures to healthy baseline..."
        python3 "${REPO_ROOT}/chaos/latency_injector.py" --reset
        ;;
    *)
        echo "Usage: $0 {payment-latency|payment-failure|db-pool-exhaust|cpu-burn|memory-leak|reset} [args]"
        echo ""
        echo "Scenarios:"
        echo "  payment-latency [ms]      Inject artificial latency into payment calls"
        echo "  payment-failure [rate]    Inject artificial HTTP 500 error rate (0.0 - 1.0)"
        echo "  db-pool-exhaust [conns]   Exhaust PostgreSQL pool slots"
        echo "  cpu-burn [seconds]        Saturate CPU cores"
        echo "  memory-leak [rate_mb]     Induce progressive memory accumulation"
        echo "  reset                     Clear all injected faults"
        exit 1
        ;;
esac
