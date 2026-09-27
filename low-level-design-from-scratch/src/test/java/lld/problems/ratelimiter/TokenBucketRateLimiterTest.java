package lld.problems.ratelimiter;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.assertj.core.api.Assertions.*;

@DisplayName("Phase 107: Token Bucket Rate Limiter Tests")
class TokenBucketRateLimiterTest {
    @Test
    void shouldAllowBurstUpToCapacity() {
        TokenBucketRateLimiter limiter = new TokenBucketRateLimiter(3, 1.0);

        assertThat(limiter.tryAcquire(1)).isTrue();
        assertThat(limiter.tryAcquire(1)).isTrue();
        assertThat(limiter.tryAcquire(1)).isTrue();
        assertThat(limiter.tryAcquire(1)).isFalse(); // Exhausted
    }
}
