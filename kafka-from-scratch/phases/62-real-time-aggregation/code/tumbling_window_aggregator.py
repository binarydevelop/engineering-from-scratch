#!/usr/bin/env python3
import time
from collections import defaultdict

class TumblingWindowAggregator:
    def __init__(self, window_size_sec=10):
        self.window_size_sec = window_size_sec
        # window_start -> { key -> count }
        self.windows = defaultdict(lambda: defaultdict(int))

    def process_event(self, key: str, timestamp_sec: float):
        window_start = int(timestamp_sec // self.window_size_sec) * self.window_size_sec
        self.windows[window_start][key] += 1

    def emit_closed_windows(self, current_time_sec: float):
        cutoff = current_time_sec - self.window_size_sec
        emitted = []
        for w_start in sorted(list(self.windows.keys())):
            if w_start < cutoff:
                emitted.append((w_start, w_start + self.window_size_sec, dict(self.windows[w_start])))
                del self.windows[w_start]
        return emitted

if __name__ == "__main__":
    agg = TumblingWindowAggregator(window_size_sec=10)
    now = 1700000000.0 # Base timestamp

    print("Feeding events into 10-second tumbling windows:")
    agg.process_event("/home", now + 1)
    agg.process_event("/home", now + 3)
    agg.process_event("/checkout", now + 4)
    agg.process_event("/home", now + 12) # Lands in window 2!

    results = agg.emit_closed_windows(now + 25)
    for start, end, counts in results:
        print(f" [Window {int(start)}-{int(end)}] Aggregations: {counts}")
