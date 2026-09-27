"""
Broken implementation demonstrating the flaw in lab-12-stale-source-freshness-sla-breach.
"""
def check_freshness(latest_ts, current_ts):
    return True # Silently passes without checking delta
