"""
Metrics from First Principles (Standard Library Only).

Implements monotonic Counters, Gauges, and Cumulative Histograms with
Prometheus exposition text formatting without external dependencies.
"""

import threading
import time
from typing import Dict, List, Tuple, Optional, Any


def _format_labels(labels: Dict[str, str]) -> str:
    if not labels:
        return ""
    items = [f'{k}="{v}"' for k, v in sorted(labels.items())]
    return "{" + ",".join(items) + "}"


class Counter:
    """
    Strictly monotonic increasing cumulative metric.
    Tracks events like requests, errors, bytes sent.
    """
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self._values: Dict[Tuple[Tuple[str, str], ...], float] = {}
        self._lock = threading.Lock()

    def inc(self, amount: float = 1.0, labels: Optional[Dict[str, str]] = None) -> None:
        if amount < 0:
            raise ValueError("Counters can only increase monotonically.")
        lbl_key = tuple(sorted((labels or {}).items()))
        with self._lock:
            self._values[lbl_key] = self._values.get(lbl_key, 0.0) + amount

    def get(self, labels: Optional[Dict[str, str]] = None) -> float:
        lbl_key = tuple(sorted((labels or {}).items()))
        with self._lock:
            return self._values.get(lbl_key, 0.0)

    def to_prometheus_text(self) -> str:
        lines = [
            f"# HELP {self.name} {self.description}",
            f"# TYPE {self.name} counter"
        ]
        with self._lock:
            for lbl_key, val in sorted(self._values.items()):
                lbl_dict = dict(lbl_key)
                lines.append(f"{self.name}{_format_labels(lbl_dict)} {val}")
        return "\n".join(lines)


class Gauge:
    """
    Arbitrary fluctuating value.
    Tracks active connections, queue depth, memory usage.
    """
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self._values: Dict[Tuple[Tuple[str, str], ...], float] = {}
        self._lock = threading.Lock()

    def set(self, value: float, labels: Optional[Dict[str, str]] = None) -> None:
        lbl_key = tuple(sorted((labels or {}).items()))
        with self._lock:
            self._values[lbl_key] = float(value)

    def inc(self, amount: float = 1.0, labels: Optional[Dict[str, str]] = None) -> None:
        lbl_key = tuple(sorted((labels or {}).items()))
        with self._lock:
            self._values[lbl_key] = self._values.get(lbl_key, 0.0) + amount

    def dec(self, amount: float = 1.0, labels: Optional[Dict[str, str]] = None) -> None:
        lbl_key = tuple(sorted((labels or {}).items()))
        with self._lock:
            self._values[lbl_key] = self._values.get(lbl_key, 0.0) - amount

    def get(self, labels: Optional[Dict[str, str]] = None) -> float:
        lbl_key = tuple(sorted((labels or {}).items()))
        with self._lock:
            return self._values.get(lbl_key, 0.0)

    def to_prometheus_text(self) -> str:
        lines = [
            f"# HELP {self.name} {self.description}",
            f"# TYPE {self.name} gauge"
        ]
        with self._lock:
            for lbl_key, val in sorted(self._values.items()):
                lbl_dict = dict(lbl_key)
                lines.append(f"{self.name}{_format_labels(lbl_dict)} {val}")
        return "\n".join(lines)


class Histogram:
    """
    Samples observations (typically request durations or payload sizes)
    and counts them into cumulative configurable buckets.
    """
    DEFAULT_BUCKETS = (0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0)

    def __init__(self, name: str, description: str, buckets: Optional[List[float]] = None):
        self.name = name
        self.description = description
        self.buckets = sorted(buckets or self.DEFAULT_BUCKETS)
        self._data: Dict[Tuple[Tuple[str, str], ...], Dict[str, Any]] = {}
        self._lock = threading.Lock()

    def observe(self, amount: float, labels: Optional[Dict[str, str]] = None) -> None:
        lbl_key = tuple(sorted((labels or {}).items()))
        with self._lock:
            if lbl_key not in self._data:
                self._data[lbl_key] = {
                    "count": 0,
                    "sum": 0.0,
                    "bucket_counts": {b: 0 for b in self.buckets}
                }
            entry = self._data[lbl_key]
            entry["count"] += 1
            entry["sum"] += amount
            for b in self.buckets:
                if amount <= b:
                    entry["bucket_counts"][b] += 1

    def to_prometheus_text(self) -> str:
        lines = [
            f"# HELP {self.name} {self.description}",
            f"# TYPE {self.name} histogram"
        ]
        with self._lock:
            for lbl_key, entry in sorted(self._data.items()):
                base_labels = dict(lbl_key)
                for b in self.buckets:
                    b_count = entry["bucket_counts"][b]
                    bucket_labels = {**base_labels, "le": str(b)}
                    lines.append(f"{self.name}_bucket{_format_labels(bucket_labels)} {b_count}")
                
                inf_labels = {**base_labels, "le": "+Inf"}
                lines.append(f"{self.name}_bucket{_format_labels(inf_labels)} {entry['count']}")
                lines.append(f"{self.name}_sum{_format_labels(base_labels)} {entry['sum']}")
                lines.append(f"{self.name}_count{_format_labels(base_labels)} {entry['count']}")
        return "\n".join(lines)


class SimpleRegistry:
    """Central metric repository for scraping."""
    def __init__(self):
        self._collectors: Dict[str, Any] = {}
        self._lock = threading.Lock()

    def register(self, collector: Any) -> None:
        with self._lock:
            self._collectors[collector.name] = collector

    def generate_prometheus_text(self) -> str:
        with self._lock:
            parts = [c.to_prometheus_text() for c in self._collectors.values()]
            return "\n\n".join(parts) + "\n"


# Global singleton registry
default_registry = SimpleRegistry()
