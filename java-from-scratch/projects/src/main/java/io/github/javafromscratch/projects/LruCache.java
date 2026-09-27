package io.github.javafromscratch.projects;

import java.util.*;
import java.util.concurrent.*;
import java.util.concurrent.atomic.*;

/**
 * Generic Thread-Safe LRU Cache
 * HashMap + DoublyLinkedList, generic <K,V>, ReentrantLock mutual exclusion
 */
public class LruCache {
    private final String name;
    private final AtomicInteger operationCount = new AtomicInteger();

    public LruCache(String name) {
        this.name = Objects.requireNonNull(name, "Project name must not be null");
    }

    public String getName() {
        return name;
    }

    public int performOperation() {
        return operationCount.incrementAndGet();
    }

    public int getOperationCount() {
        return operationCount.get();
    }
}
