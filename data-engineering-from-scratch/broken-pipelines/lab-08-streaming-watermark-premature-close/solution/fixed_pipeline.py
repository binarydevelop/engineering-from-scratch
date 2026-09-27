"""
Resilient, production-ready solution for lab-08-streaming-watermark-premature-close.
"""
def is_late_watermarked(event_time, high_watermark, allowed_lateness_sec=60):
    return event_time < (high_watermark - allowed_lateness_sec)
