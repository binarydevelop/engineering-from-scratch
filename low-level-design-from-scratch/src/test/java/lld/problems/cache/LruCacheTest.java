package lld.problems.cache;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.assertj.core.api.Assertions.*;

@DisplayName("Phase 106: LRU Cache Implementation Tests")
class LruCacheTest {
    @Test
    void shouldStoreAndRetrieveKeys() {
        LruCache<String, Integer> cache = new LruCache<>(2);
        cache.put("A", 1);
        cache.put("B", 2);

        assertThat(cache.get("A")).contains(1);
        assertThat(cache.get("B")).contains(2);
    }

    @Test
    void shouldEvictLeastRecentlyUsedKeyWhenCapacityExceeded() {
        LruCache<String, Integer> cache = new LruCache<>(2);
        cache.put("A", 1);
        cache.put("B", 2);

        // Access A to make B least recently used
        cache.get("A");

        // Insert C; B should be evicted
        cache.put("C", 3);

        assertThat(cache.get("A")).contains(1);
        assertThat(cache.get("C")).contains(3);
        assertThat(cache.get("B")).isEmpty();
    }
}
