package lld.concurrency.inventory;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicInteger;

import static org.assertj.core.api.Assertions.*;

@DisplayName("Phase 71 & 72: Thread Safe Inventory Concurrency Tests")
class ThreadSafeInventoryTest {

    @Test
    @DisplayName("Should prevent double-booking under concurrent multithreaded contention")
    void shouldPreventOverbookingUnderHighContention() throws InterruptedException {
        ThreadSafeInventory inventory = new ThreadSafeInventory();
        inventory.addStock("IPHONE-15", 50);

        int threads = 200;
        ExecutorService executor = Executors.newFixedThreadPool(threads);
        CountDownLatch latch = new CountDownLatch(1);
        AtomicInteger successfulReservations = new AtomicInteger(0);

        for (int i = 0; i < threads; i++) {
            executor.submit(() -> {
                try {
                    latch.await();
                    if (inventory.reserveStock("IPHONE-15", 1)) {
                        successfulReservations.incrementAndGet();
                    }
                } catch (InterruptedException ignored) {}
            });
        }

        latch.countDown();
        executor.shutdown();
        boolean finished = executor.awaitTermination(5, TimeUnit.SECONDS);

        assertThat(finished).isTrue();
        assertThat(successfulReservations.get()).isEqualTo(50);
        assertThat(inventory.getAvailableStock("IPHONE-15")).isZero();
    }
}
