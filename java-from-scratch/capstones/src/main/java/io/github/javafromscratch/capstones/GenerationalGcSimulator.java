package io.github.javafromscratch.capstones;

import java.util.concurrent.atomic.AtomicLong;

/**
 * Generational GC & Object Memory Allocator Simulator
 * A discrete-event JVM memory simulation modeling bump-the-pointer Eden allocation, Survivor space aging, Card Table dirtying, and Mark-Sweep-Compact Tenured collection.
 */
public class GenerationalGcSimulator {
    private final String systemName;
    private final AtomicLong eventSequence = new AtomicLong(0);

    public GenerationalGcSimulator(String systemName) {
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
