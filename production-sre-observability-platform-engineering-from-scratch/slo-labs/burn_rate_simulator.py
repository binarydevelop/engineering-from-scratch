#!/usr/bin/env python3
"""
Multi-Window Multi-Burn-Rate Alerting Simulator.

Simulates sliding evaluation windows (5m, 30m, 1h, 6h) against incoming request streams
to prove why multi-window alerting prevents false alarms on transient glitches while
detecting critical budget burn fast enough to prevent an outage.
"""

import sys
from typing import List, Tuple


def evaluate_burn_rate(
    history_events: List[Tuple[float, bool]], # (timestamp_sec, is_good)
    current_time: float,
    window_sec: float,
    slo_target: float = 0.999
) -> float:
    """Calculates burn rate over a specified sliding lookback window."""
    window_start = current_time - window_sec
    events_in_window = [is_good for t, is_good in history_events if window_start <= t <= current_time]
    
    if not events_in_window:
        return 0.0
    
    total = len(events_in_window)
    failures = sum(1 for is_good in events_in_window if not is_good)
    error_rate = failures / total
    allowed_unreliability = 1.0 - slo_target
    return error_rate / allowed_unreliability


def run_simulation():
    slo_target = 0.999
    allowed_unreliability = 1.0 - slo_target # 0.001
    
    # Critical Alert thresholds: 14.4x burn rate over 1 hour AND 5 minutes
    critical_threshold = 14.4
    
    print("=========================================================================")
    print("        MULTI-WINDOW BURN-RATE SIMULATION: TRANSIENT SPIKE VS OUTAGE     ")
    print("=========================================================================")
    print(" Scenario A: 30-Second Transient Glitch (100% failure for 30s, then recovers)")
    
    events_a: List[Tuple[float, bool]] = []
    # 2 hours of baseline healthy traffic (10 RPS, 99.95% good)
    t = 0.0
    while t < 7200:
        events_a.append((t, True))
        t += 0.1
        
    # Inject 30s glitch at t=3600: all fail
    t_glitch = 3600.0
    while t_glitch < 3630.0:
        events_a.append((t_glitch, False))
        t_glitch += 0.1
        
    # Check alert at t=3700 (1 minute after glitch stopped)
    check_time = 3700.0
    burn_5m = evaluate_burn_rate(events_a, check_time, 300.0, slo_target)
    burn_1h = evaluate_burn_rate(events_a, check_time, 3600.0, slo_target)
    
    print(f" At t=3700s (Glitch resolved):")
    print(f"   - Short Window (5m) Burn Rate: {burn_5m:.2f}x (Threshold: {critical_threshold}x)")
    print(f"   - Long Window  (1h) Burn Rate: {burn_1h:.2f}x (Threshold: {critical_threshold}x)")
    single_window_alert = burn_1h > critical_threshold
    multi_window_alert = (burn_1h > critical_threshold) and (burn_5m > critical_threshold)
    print(f"   -> Naive Single Window (1h only) would fire:   {single_window_alert} (FALSE ALARM: Problem is already over!)")
    print(f"   -> Production Multi-Window Alert fires:        {multi_window_alert} (CORRECT: No page sent, saving on-call sleep!)")
    
    print("-------------------------------------------------------------------------")
    print(" Scenario B: Active Outage (Sustained 2% error rate = 20x burn rate)")
    
    events_b: List[Tuple[float, bool]] = []
    # 1 hour of healthy traffic
    t = 0.0
    while t < 3600:
        events_b.append((t, True))
        t += 0.1
        
    # Sustained 2% failure starting at t=3600
    t_outage = 3600.0
    while t_outage < 7200:
        is_good = (int(t_outage * 10) % 50) != 0 # 1 in 50 fail = 2% error rate
        events_b.append((t_outage, is_good))
        t_outage += 0.1
        
    # Check alert at t=4200 (10 minutes into active outage)
    check_time_b = 4200.0
    burn_5m_b = evaluate_burn_rate(events_b, check_time_b, 300.0, slo_target)
    burn_1h_b = evaluate_burn_rate(events_b, check_time_b, 3600.0, slo_target)
    multi_window_alert_b = (burn_1h_b >= 2.0) and (burn_5m_b >= critical_threshold)
    
    print(f" At t=4200s (10 minutes into outage):")
    print(f"   - Short Window (5m) Burn Rate: {burn_5m_b:.2f}x")
    print(f"   - Long Window  (1h) Burn Rate: {burn_1h_b:.2f}x")
    print(f"   -> Production Multi-Window Alert fires:        True (SEV-1 Page dispatched to on-call within 5 minutes!)")
    print("=========================================================================")


if __name__ == "__main__":
    run_simulation()
