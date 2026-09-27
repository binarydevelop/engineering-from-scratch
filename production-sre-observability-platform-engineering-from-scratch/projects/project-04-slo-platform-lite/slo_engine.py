"""
Project 04: SLO Engine & Multi-Window Burn Rate Evaluator.
"""
from typing import Dict, Any

class SLOEngine:
    def __init__(self, target_slo: float = 0.999, window_days: int = 30):
        self.target_slo = target_slo
        self.window_days = window_days
        self.error_budget = 1.0 - target_slo

    def calculate_burn_rate(self, current_error_rate: float) -> float:
        """
        Burn rate = (Current Error Rate) / (Allowed Error Budget).
        Burn rate 1.0 consumes 100% of budget over the full window.
        Burn rate 14.4 consumes 2% of budget in 1 hour.
        """
        if self.error_budget <= 0: return 0.0
        return current_error_rate / self.error_budget

    def evaluate_alert(self, burn_rate_1h: float, burn_rate_6h: float) -> Dict[str, Any]:
        # Google SRE Workbook multi-window multi-burn-rate criteria:
        # Page: 1h burn > 14.4 and 6h burn > 6.0
        should_page = (burn_rate_1h > 14.4 and burn_rate_6h > 6.0)
        should_ticket = (burn_rate_1h > 3.0 and burn_rate_6h > 1.0)
        return {
            "should_page": should_page,
            "should_ticket": should_ticket and not should_page,
            "burn_rate_1h": burn_rate_1h
        }
