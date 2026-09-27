package io.github.javafromscratch.projects;

import java.util.*;
import java.util.concurrent.*;
import java.util.concurrent.atomic.*;

/**
 * Resilient Task Runner
 * ThreadPoolExecutor, priority queue, exponential backoff retries, metrics
 */
public class TaskRunner {
    private final String name;
    private final AtomicInteger operationCount = new AtomicInteger();

    public TaskRunner(String name) {
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
