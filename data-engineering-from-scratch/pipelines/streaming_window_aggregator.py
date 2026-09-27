#!/usr/bin/env python3
"""
pipelines/streaming_window_aggregator.py
Event-Time Tumbling Window Aggregator:
Processes continuous stream of events, tracks high-watermark, groups by 5-minute event windows,
and manages late-arriving events according to watermark lag tolerance.
"""
import json
from pathlib import Path
from datetime import datetime, timezone, timedelta
from collections import defaultdict

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "datasets" / "raw"

class TumblingWindowAggregator:
    def __init__(self, window_size_seconds=300, max_lateness_seconds=60):
        self.window_size = timedelta(seconds=window_size_seconds)
        self.max_lateness = timedelta(seconds=max_lateness_seconds)
        self.watermark = datetime.min.replace(tzinfo=timezone.utc)
        self.windows = defaultdict(lambda: {"event_count": 0, "actions": defaultdict(int)})
        self.closed_windows = set()
        self.late_events_dropped = 0

    def parse_event_time(self, ts_str):
        # Support ISO 8601 UTC
        if ts_str.endswith("Z"):
            ts_str = ts_str[:-1] + "+00:00"
        return datetime.fromisoformat(ts_str)

    def get_window_start(self, event_time):
        epoch = datetime(1970, 1, 1, tzinfo=timezone.utc)
        total_seconds = int((event_time - epoch).total_seconds())
        window_seconds = int(self.window_size.total_seconds())
        window_start_sec = (total_seconds // window_seconds) * window_seconds
        return epoch + timedelta(seconds=window_start_sec)

    def process_event(self, event):
        event_time = self.parse_event_time(event["event_timestamp"])

        # Update high-watermark (high event time minus tolerated lateness)
        candidate_watermark = event_time - self.max_lateness
        if candidate_watermark > self.watermark:
            self.watermark = candidate_watermark

        window_start = self.get_window_start(event_time)

        # Check if window is already finalized (late event)
        if event_time < self.watermark:
            self.late_events_dropped += 1
            return False, "LATE_EVENT_DROPPED"

        # Accumulate state inside active window
        self.windows[window_start]["event_count"] += 1
        self.windows[window_start]["actions"][event["action"]] += 1
        return True, "ACCUMULATED"

    def finalize_closed_windows(self):
        ready = []
        for w_start, metrics in list(self.windows.items()):
            w_end = w_start + self.window_size
            if w_end <= self.watermark and w_start not in self.closed_windows:
                self.closed_windows.add(w_start)
                ready.append({
                    "window_start": w_start.isoformat(),
                    "window_end": w_end.isoformat(),
                    "event_count": metrics["event_count"],
                    "actions": dict(metrics["actions"])
                })
        return ready

def run_streaming_aggregation(stream_file=None):
    if stream_file is None:
        stream_file = RAW_DIR / "clickstream.jsonl"

    print("Starting Streaming Tumbling Window Aggregator...")
    aggregator = TumblingWindowAggregator(window_size_seconds=300, max_lateness_seconds=30)

    total_processed = 0
    with open(stream_file, "r") as f:
        for line in f:
            if not line.strip():
                continue
            event = json.loads(line)
            aggregator.process_event(event)
            total_processed += 1

    # Advance watermark to close trailing windows
    aggregator.watermark = datetime.max.replace(tzinfo=timezone.utc)
    closed = aggregator.finalize_closed_windows()

    print(f"Stream processing finished.")
    print(f"  Total events processed: {total_processed}")
    print(f"  Late events dropped: {aggregator.late_events_dropped}")
    print(f"  Windows materialized: {len(closed)}")

    for i, w in enumerate(closed[:3], 1):
        print(f"  [Window {i}] {w['window_start']} to {w['window_end']}: {w['event_count']} events")

    return closed

if __name__ == "__main__":
    run_streaming_aggregation()
