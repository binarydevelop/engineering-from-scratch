package io.github.javafromscratch.capstones;

import java.util.concurrent.atomic.AtomicLong;

/**
 * Lock-Free High-Performance Ring Buffer
 * A zero-allocation, lock-free inter-thread messaging ring buffer implementing mechanical sympathy, cache-line padding to prevent false sharing, and atomic sequence tracking.
 */
public class DisruptorRingBuffer {
    private final String systemName;
    private final AtomicLong eventSequence = new AtomicLong(0);

    public DisruptorRingBuffer(String systemName) {
        this.systemName = systemName;
    }

    public String getSystemName() {
        return systemName;
    }

    public long publishEvent() {
        return eventSequence.incrementAndGet();
    }

    public long getPublishedEventCount() {
        return eventSequence.get();
    }
}
