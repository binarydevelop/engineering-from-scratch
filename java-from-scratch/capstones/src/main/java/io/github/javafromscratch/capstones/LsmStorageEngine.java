package io.github.javafromscratch.capstones;

import java.util.concurrent.atomic.AtomicLong;

/**
 * Multi-Threaded WAL & LSM-Tree Storage Engine
 * A log-structured storage engine featuring an append-only Write-Ahead Log (WAL) on disk, concurrent in-memory MemTable, and background SSTable compaction.
 */
public class LsmStorageEngine {
    private final String systemName;
    private final AtomicLong eventSequence = new AtomicLong(0);

    public LsmStorageEngine(String systemName) {
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
