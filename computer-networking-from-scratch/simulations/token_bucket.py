#!/usr/bin/env python3
"""
simulations/token_bucket.py
Simulates the Token Bucket algorithm used for traffic shaping and bandwidth limiting (e.g. Linux tc tbf).
Key parameters:
  - Rate (r): tokens added per second (bandwidth limit in bytes/sec)
  - Capacity (b): bucket size (maximum allowable burst in bytes)
"""

import time
from typing import Optional, Tuple


class TokenBucket:
    def __init__(self, rate_bytes_per_sec: float, capacity_bytes: float, initial_time: Optional[float] = None):
        self.rate = rate_bytes_per_sec
        self.capacity = capacity_bytes
        self.tokens = capacity_bytes
        self.last_update = initial_time if initial_time is not None else time.time()

    def consume(self, num_bytes: float, current_time: Optional[float] = None) -> Tuple[bool, float]:
        """
        Attempts to consume num_bytes tokens.
        Returns: (allowed: bool, current_tokens: float)
        """
        now = current_time if current_time is not None else time.time()
        elapsed = max(0.0, now - self.last_update)
        self.last_update = now

        # Replenish tokens based on elapsed time up to capacity
        self.tokens = min(self.capacity, self.tokens + (elapsed * self.rate))

        if self.tokens >= num_bytes:
            self.tokens -= num_bytes
            return True, self.tokens
        else:
            # Insufficient tokens: traffic throttled/dropped
            return False, self.tokens


if __name__ == "__main__":
    # Bandwidth limit: 100 KB/s (100,000 bytes/sec), Burst capacity: 200 KB
    rate = 100_000
    burst = 200_000
    bucket = TokenBucket(rate_bytes_per_sec=rate, capacity_bytes=burst)
    t = 0.0
    bucket.last_update = t

    print(f"Token Bucket Traffic Shaper (Rate={rate/1000:.0f} KB/s, Burst={burst/1000:.0f} KB):")
    print("=" * 65)

    # 1. Initial burst of 150 KB
    ok, rem = bucket.consume(150_000, current_time=t)
    print(f"t={t:.2f}s: Packet 1 (150 KB) -> Allowed: {ok} (Remaining tokens: {rem/1000:.1f} KB)")
    assert ok is True

    # 2. Immediate second burst of 100 KB (Only 50 KB left)
    ok, rem = bucket.consume(100_000, current_time=t)
    print(f"t={t:.2f}s: Packet 2 (100 KB) -> Allowed: {ok} (Remaining tokens: {rem/1000:.1f} KB) [THROTTLED]")
    assert ok is False

    # 3. Advance time by 0.6 seconds (60 KB added -> 50 + 60 = 110 KB tokens)
    t += 0.6
    ok, rem = bucket.consume(100_000, current_time=t)
    print(f"t={t:.2f}s: Packet 3 (100 KB) -> Allowed: {ok} (Remaining tokens: {rem/1000:.1f} KB) [ALLOWED]")
    assert ok is True

    print("\nSUCCESS: Token bucket traffic rate limiting verified.")
