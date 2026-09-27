#!/usr/bin/env python3
import statistics

class MetricAccumulator:
    def __init__(self):
        self.count = 0
        self.total = 0.0
        self.min_val = float('inf')
        self.max_val = float('-inf')
        self.values = []

    def add(self, val):
        self.count += 1
        self.total += val
        if val < self.min_val: self.min_val = val
        if val > self.max_val: self.max_val = val
        self.values.append(val)

    def stats(self):
        avg = self.total / self.count if self.count > 0 else 0.0
        return {
            "count": self.count,
            "min": self.min_val,
            "max": self.max_val,
            "avg": round(avg, 2),
            "p95": round(statistics.quantiles(self.values, n=100)[94], 2) if len(self.values) >= 100 else None
        }

if __name__ == "__main__":
    acc = MetricAccumulator()
    import random
    random.seed(42)
    for _ in range(1000):
        acc.add(random.uniform(10.0, 500.0))
    print("Computed Streaming Metric Stats:")
    for k, v in acc.stats().items():
        print(f"  {k:10s}: {v}")
