"""
Broken implementation demonstrating the flaw in lab-08-streaming-watermark-premature-close.
"""
def is_late_naive(event_time, wall_clock):
    return event_time < wall_clock # Drops any event with even 1s network latency!
