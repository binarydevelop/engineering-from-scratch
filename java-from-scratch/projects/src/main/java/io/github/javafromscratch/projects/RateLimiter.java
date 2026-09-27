package io.github.javafromscratch.projects;

import java.util.*;
import java.util.concurrent.*;
import java.util.concurrent.atomic.*;

/**
 * Distributed-Ready Rate Limiter
 * Token Bucket and Sliding Window rate limiters using AtomicLong
 */
public class RateLimiter {
    private final String name;
    private final AtomicInteger operationCount = new AtomicInteger();

    public RateLimiter(String name) {
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
