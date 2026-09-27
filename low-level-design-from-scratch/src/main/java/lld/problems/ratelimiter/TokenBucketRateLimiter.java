package lld.problems.ratelimiter;

public class TokenBucketRateLimiter {
    private final long capacity;
    private final double refillRatePerSecond;
    private double currentTokens;
    private long lastRefillTimestampNanos;

    public TokenBucketRateLimiter(long capacity, double refillRatePerSecond) {
        if (capacity <= 0 || refillRatePerSecond <= 0) {
            throw new IllegalArgumentException("Capacity and refill rate must be positive");
        }
        this.capacity = capacity;
        this.refillRatePerSecond = refillRatePerSecond;
        this.currentTokens = capacity;
        this.lastRefillTimestampNanos = System.nanoTime();
    }

    public synchronized boolean tryAcquire(long tokens) {
        refill();
        if (currentTokens >= tokens) {
            currentTokens -= tokens;
            return true;
        }
        return false;
    }

    private void refill() {
        long now = System.nanoTime();
        double elapsedSeconds = (now - lastRefillTimestampNanos) / 1_000_000_000.0;
        currentTokens = Math.min(capacity, currentTokens + (elapsedSeconds * refillRatePerSecond));
        lastRefillTimestampNanos = now;
    }
}
