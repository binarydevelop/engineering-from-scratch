#!/usr/bin/env python3
import time
import random

def retry_with_backoff(operation_fn, max_retries=5, base_delay=0.1, max_delay=2.0):
    for attempt in range(max_retries):
        try:
            return operation_fn(attempt)
        except Exception as e:
            if attempt == max_retries - 1:
                raise e
            # Exponential backoff + full jitter
            delay = min(max_delay, base_delay * (2 ** attempt))
            jitter = random.uniform(0, delay)
            print(f"  Attempt {attempt + 1} rejected ({e}). Backing off for {jitter:.3f}s...")
            time.sleep(jitter)

if __name__ == "__main__":
    def flaky_write(attempt):
        if attempt < 2:
            raise RuntimeError("HTTP 429: EsRejectedExecutionException (Write Queue Full)")
        return "HTTP 200 OK: Bulk Indexed Successfully"

    print("Simulating Client-Side Retry with Exponential Backoff & Jitter:")
    result = retry_with_backoff(flaky_write)
    print("Final Result:", result)
