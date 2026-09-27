#!/usr/bin/env python3
"""
projects/03-rate-limiter/limiter.py — Distributed Rate Limiting Engines

Implements and compares three architectures:
1. Fixed Window Counter: Lightweight, vulnerable to 2x boundary spikes
2. Sliding Window Log: Perfectly accurate, memory overhead scales with request count
3. Token Bucket (Atomic Lua): Smooth bursting, constant memory, rate-refill mechanics
"""

import socket
import time

REDIS_HOST = "localhost"
REDIS_PORT = 6379

def redis_cmd(*args):
    s = socket.create_connection((REDIS_HOST, REDIS_PORT), timeout=2.0)
    msg = f"*{len(args)}\r\n"
    for arg in args:
        s_arg = str(arg)
        msg += f"${len(s_arg.encode('utf-8'))}\r\n{s_arg}\r\n"
    s.sendall(msg.encode("utf-8"))
    
    resp = s.recv(4096).decode("utf-8", errors="replace")
    s.close()
    return resp

class FixedWindowLimiter:
    """
    Counts requests per discrete time window (e.g. second or minute).
    Risk: 10 requests at second 0.99 and 10 requests at second 1.01 = 20 requests in 20ms!
    """
    def __init__(self, limit=10, window_sec=1):
        self.limit = limit
        self.window = window_sec

    def allow(self, user_id):
        current_window = int(time.time() // self.window)
        key = f"rate:fixed:{user_id}:{current_window}"
        raw = redis_cmd("INCR", key)
        count = int(raw.split("\r\n")[0][1:])
        if count == 1:
            redis_cmd("EXPIRE", key, self.window * 2)
        return count <= self.limit, count

class SlidingWindowLogLimiter:
    """
    Uses Redis Sorted Set.
    Score = timestamp (float milliseconds)
    Member = unique request ID
    Prunes elements older than now - window.
    """
    def __init__(self, limit=10, window_sec=1):
        self.limit = limit
        self.window_ms = window_sec * 1000

    def allow(self, user_id):
        now_ms = time.time() * 1000
        key = f"rate:sliding:{user_id}"
        cutoff = now_ms - self.window_ms
        
        # 1. Remove expired timestamps
        redis_cmd("ZREMRANGEBYSCORE", key, "-inf", str(cutoff))
        # 2. Add current timestamp
        req_id = f"{now_ms}_{time.perf_counter()}"
        redis_cmd("ZADD", key, str(now_ms), req_id)
        # 3. Set TTL to prevent abandoned keys
        redis_cmd("PEXPIRE", key, str(int(self.window_ms * 2)))
        # 4. Count remaining
        raw = redis_cmd("ZCARD", key)
        count = int(raw.split("\r\n")[0][1:])
        return count <= self.limit, count

class TokenBucketLimiter:
    """
    Atomic Token Bucket via Redis Lua Script.
    Maintains last_refill timestamp and available token count in a Redis Hash.
    Refills at constant rate: (now - last_refill) * refill_rate
    """
    LUA_SCRIPT = """
    local key = KEYS[1]
    local capacity = tonumber(ARGV[1])
    local refill_rate = tonumber(ARGV[2]) -- tokens per millisecond
    local now = tonumber(ARGV[3])
    local requested = tonumber(ARGV[4])

    local data = redis.call("HMGET", key, "tokens", "last_updated")
    local tokens = tonumber(data[1])
    local last_updated = tonumber(data[2])

    if tokens == nil then
        tokens = capacity
        last_updated = now
    else
        local elapsed = math.max(0, now - last_updated)
        local added = elapsed * refill_rate
        tokens = math.min(capacity, tokens + added)
        last_updated = now
    end

    if tokens >= requested then
        tokens = tokens - requested
        redis.call("HMSET", key, "tokens", tokens, "last_updated", last_updated)
        redis.call("PEXPIRE", key, math.ceil((capacity / refill_rate) * 2))
        return {1, math.floor(tokens)}
    else
        redis.call("HMSET", key, "tokens", tokens, "last_updated", last_updated)
        redis.call("PEXPIRE", key, math.ceil((capacity / refill_rate) * 2))
        return {0, math.floor(tokens)}
    end
    """

    def __init__(self, capacity=10, refill_per_sec=5):
        self.capacity = capacity
        self.refill_rate = refill_per_sec / 1000.0 # tokens / ms

    def allow(self, user_id, requested=1):
        key = f"rate:tokenbucket:{user_id}"
        now_ms = int(time.time() * 1000)
        raw = redis_cmd("EVAL", self.LUA_SCRIPT, "1", key, str(self.capacity),
                        str(self.refill_rate), str(now_ms), str(requested))
        # Parse RESP array return {allowed, remaining}
        lines = [l for l in raw.split("\r\n") if l.startswith(":")]
        if len(lines) >= 2:
            allowed = lines[0] == ":1"
            remaining = int(lines[1][1:])
            return allowed, remaining
        return False, 0

if __name__ == "__main__":
    print("Testing Rate Limiters with 15 rapid-fire requests (Limit: 5 requests/sec)...")
    limiters = [
        ("Fixed Window (limit=5)", FixedWindowLimiter(limit=5, window_sec=1)),
        ("Sliding Window Log (limit=5)", SlidingWindowLogLimiter(limit=5, window_sec=1)),
        ("Token Bucket (capacity=5, refill=2/s)", TokenBucketLimiter(capacity=5, refill_per_sec=2))
    ]

    for name, lim in limiters:
        print(f"\n--- {name} ---")
        accepted = 0
        rejected = 0
        for i in range(1, 11):
            ok, val = lim.allow("user_test")
            status = "✓ ALLOWED" if ok else "✗ REJECTED (429)"
            print(f"  Req #{i:2d}: {status} (State: {val})")
            if ok: accepted += 1
            else: rejected += 1
            time.sleep(0.05)
        print(f"Result: {accepted} Accepted, {rejected} Throttled")
