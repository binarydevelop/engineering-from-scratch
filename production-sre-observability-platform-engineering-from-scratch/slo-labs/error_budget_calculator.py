#!/usr/bin/env python3
"""
Production Error Budget & Burn Rate Calculator.

Calculates error budgets, time to exhaustion, and multi-window burn rates
from first principles without external dependencies.
"""

import sys
import argparse
from typing import Dict, Any


def calculate_error_budget(
    total_requests: int,
    failed_requests: int,
    slo_target: float = 0.999,
    window_days: int = 30
) -> Dict[str, Any]:
    """
    Computes complete error budget dynamics.
    """
    if total_requests <= 0:
        return {"error": "Total requests must be > 0"}

    actual_reliability = (total_requests - failed_requests) / total_requests
    allowed_unreliability = 1.0 - slo_target
    allowed_failures = int(total_requests * allowed_unreliability)
    
    consumed_budget = failed_requests / allowed_failures if allowed_failures > 0 else 0.0
    remaining_budget_percent = max(0.0, (1.0 - consumed_budget) * 100.0)

    # Current error rate
    error_rate = failed_requests / total_requests
    burn_rate = round(error_rate / allowed_unreliability, 4) if allowed_unreliability > 0 else 0.0

    # Time to exhaust remaining budget if current burn rate continues
    window_hours = window_days * 24.0
    if burn_rate > 0:
        hours_to_exhaust = (remaining_budget_percent / 100.0) * (window_hours / burn_rate)
    else:
        hours_to_exhaust = float("inf")

    return {
        "slo_target_percent": slo_target * 100.0,
        "actual_reliability_percent": actual_reliability * 100.0,
        "total_requests": total_requests,
        "allowed_failures": allowed_failures,
        "actual_failures": failed_requests,
        "consumed_budget_percent": consumed_budget * 100.0,
        "remaining_budget_percent": remaining_budget_percent,
        "burn_rate": burn_rate,
        "hours_to_exhaust": hours_to_exhaust,
        "slo_status": "COMPLIANT" if actual_reliability >= slo_target else "BREACHED"
    }


def main():
    parser = argparse.ArgumentParser(description="Production Error Budget & Burn Rate Calculator")
    parser.add_argument("--total-requests", type=int, default=10000000, help="Total requests in window")
    parser.add_argument("--failed-requests", type=int, default=4500, help="Failed or slow requests")
    parser.add_argument("--slo-target", type=float, default=0.999, help="SLO target (e.g. 0.999 for 99.9%%)")
    parser.add_argument("--window-days", type=int, default=30, help="Rolling window in days")

    args = parser.parse_args()
    results = calculate_error_budget(
        total_requests=args.total_requests,
        failed_requests=args.failed_requests,
        slo_target=args.slo_target,
        window_days=args.window_days
    )

    print("=================================================================")
    print("           PRODUCTION ERROR BUDGET ASSESSMENT REPORT             ")
    print("=================================================================")
    print(f" SLO Target:               {results['slo_target_percent']:.3f}% ({args.window_days}-day rolling window)")
    print(f" Actual Reliability:       {results['actual_reliability_percent']:.4f}%")
    print(f" SLO Compliance Status:    {results['slo_status']}")
    print("-----------------------------------------------------------------")
    print(f" Total Eligible Requests:  {results['total_requests']:,}")
    print(f" Total Allowed Failures:   {results['allowed_failures']:,}")
    print(f" Actual Failures Incurred: {results['actual_failures']:,}")
    print("-----------------------------------------------------------------")
    print(f" Consumed Error Budget:    {results['consumed_budget_percent']:.2f}%")
    print(f" Remaining Error Budget:   {results['remaining_budget_percent']:.2f}%")
    print(f" Current Burn Rate:        {results['burn_rate']:.2f}x")
    if results['hours_to_exhaust'] == float("inf"):
        print(" Time to Total Exhaustion: Infinite (No active failures)")
    else:
        print(f" Time to Total Exhaustion: {results['hours_to_exhaust']:.1f} hours ({results['hours_to_exhaust']/24:.1f} days)")
    print("=================================================================")


if __name__ == "__main__":
    main()
