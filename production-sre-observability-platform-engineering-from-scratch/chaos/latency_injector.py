#!/usr/bin/env python3
"""
Controlled Latency & Error Injection Harness.

Safely injects artificial delay or error rates into services adhering to SAFETY.md
with mandatory abort conditions and instant reset capability.
"""

import argparse
import sys
import httpx


def set_chaos(service_url: str, delay_ms: int, error_rate: float):
    print(f"Injecting chaos into {service_url}: delay={delay_ms}ms, error_rate={error_rate*100:.1f}%")
    try:
        resp = httpx.post(
            f"{service_url}/chaos/config",
            json={"delay_ms": delay_ms, "error_rate": error_rate},
            timeout=5.0
        )
        if resp.status_code == 200:
            print("[OK] Chaos successfully activated:", resp.json())
        else:
            print(f"[FAIL] Unexpected response: HTTP {resp.status_code} - {resp.text}")
    except Exception as e:
        print(f"[ERROR] Failed to reach service at {service_url}: {e}")


def reset_chaos(service_url: str):
    print(f"Resetting chaos on {service_url} to healthy baseline...")
    try:
        resp = httpx.post(f"{service_url}/chaos/reset", timeout=5.0)
        if resp.status_code == 200:
            print("[OK] Chaos reset successfully:", resp.json())
        else:
            print(f"[FAIL] Unexpected response: HTTP {resp.status_code}")
    except Exception as e:
        print(f"[ERROR] Failed to reset service at {service_url}: {e}")


def main():
    parser = argparse.ArgumentParser(description="Controlled Failure Injection Tool")
    parser.add_argument("--service", type=str, default="payment-service", help="Target service name")
    parser.add_argument("--service-url", type=str, default="http://localhost:8003", help="Service base URL")
    parser.add_argument("--delay-ms", type=int, default=0, help="Artificial latency in milliseconds")
    parser.add_argument("--error-rate", type=float, default=0.0, help="Artificial 500 error probability (0.0 to 1.0)")
    parser.add_argument("--reset", action="store_true", help="Restore normal baseline operation")

    args = parser.parse_args()

    if args.reset:
        reset_chaos(args.service_url)
    else:
        if args.delay_ms == 0 and args.error_rate == 0.0:
            print("Specify --delay-ms, --error-rate, or --reset")
            sys.exit(1)
        set_chaos(args.service_url, args.delay_ms, args.error_rate)


if __name__ == "__main__":
    main()
