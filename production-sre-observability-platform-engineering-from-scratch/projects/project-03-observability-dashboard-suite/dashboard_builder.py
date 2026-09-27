"""
Project 03: Dashboard Suite Generator for RED and USE Metrics.
"""
from typing import Dict, Any

class DashboardBuilder:
    @staticmethod
    def build_red_dashboard(service_name: str) -> Dict[str, Any]:
        return {
            "title": f"RED Signals - {service_name}",
            "panels": [
                {
                    "title": "Rate (RPS)",
                    "type": "graph",
                    "query": f'sum(rate(http_requests_total{{service="{service_name}"}}[1m]))'
                },
                {
                    "title": "Errors (5xx Rate)",
                    "type": "graph",
                    "query": f'sum(rate(http_requests_total{{service="{service_name}",status=~"5.."}}[1m]))'
                },
                {
                    "title": "Duration (p95 & p99 Latency)",
                    "type": "graph",
                    "query": f'histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket{{service="{service_name}"}}[5m])) by (le))'
                }
            ]
        }
