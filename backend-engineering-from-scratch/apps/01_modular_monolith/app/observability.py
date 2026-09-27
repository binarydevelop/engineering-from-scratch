"""
Observability module: RED metrics (Rate, Errors, Duration) and correlation tracking.
"""

import time
import uuid
import json
from typing import Dict, List, Any

class REDMetrics:
    def __init__(self):
        self.request_count = 0
        self.error_count = 0
        self.latencies: List[float] = []

    def record_request(self, duration_sec: float, status_code: int):
        self.request_count += 1
        self.latencies.append(duration_sec)
        if status_code >= 400:
            self.error_count += 1

    def summary(self) -> Dict[str, Any]:
        count = len(self.latencies)
        avg_lat = sum(self.latencies) / count if count > 0 else 0.0
        sorted_lat = sorted(self.latencies)
        p50 = sorted_lat[int(0.50 * count)] if count > 0 else 0.0
        p99 = sorted_lat[int(0.99 * count)] if count > 0 else 0.0
        return {
            "rate_total_requests": self.request_count,
            "errors_total": self.error_count,
            "error_rate": (self.error_count / self.request_count) if self.request_count > 0 else 0.0,
            "duration_avg_sec": round(avg_lat, 4),
            "duration_p50_sec": round(p50, 4),
            "duration_p99_sec": round(p99, 4),
        }

class StructuredLogger:
    @staticmethod
    def log(level: str, message: str, correlation_id: str = "", **kwargs) -> str:
        entry = {
            "timestamp": time.time(),
            "level": level.upper(),
            "correlation_id": correlation_id or str(uuid.uuid4()),
            "message": message,
            **kwargs
        }
        return json.dumps(entry)
