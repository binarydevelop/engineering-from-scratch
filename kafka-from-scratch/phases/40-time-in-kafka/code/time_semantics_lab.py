#!/usr/bin/env python3
import time
from datetime import datetime

def test_time_semantics():
    # 1. Real-world event occurs
    event_time_ms = int(time.time() * 1000) - 300000 # 5 minutes ago
    event_dt = datetime.fromtimestamp(event_time_ms / 1000)

    # 2. Broker receives and writes
    log_append_time_ms = int(time.time() * 1000)
    append_dt = datetime.fromtimestamp(log_append_time_ms / 1000)

    # 3. Consumer processes later
    processing_time_ms = log_append_time_ms + 10000 # 10s later
    process_dt = datetime.fromtimestamp(processing_time_ms / 1000)

    print("Timestamp Analysis for Record:")
    print(f"  Event Time (CreateTime):   {event_dt.strftime('%H:%M:%S')} (When event physically happened)")
    print(f"  Log Append Time:           {append_dt.strftime('%H:%M:%S')} (When broker committed to disk)")
    print(f"  Processing Time:           {process_dt.strftime('%H:%M:%S')} (When consumer thread executed)")
    print(f"\nTime Delta (Ingestion Delay):  {(log_append_time_ms - event_time_ms)/1000:.1f} seconds")
    print(f"Time Delta (Processing Lag):   {(processing_time_ms - log_append_time_ms)/1000:.1f} seconds")

if __name__ == "__main__":
    test_time_semantics()
