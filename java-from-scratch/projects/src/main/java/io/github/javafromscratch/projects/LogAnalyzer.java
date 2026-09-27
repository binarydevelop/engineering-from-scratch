package io.github.javafromscratch.projects;

import java.util.*;
import java.util.concurrent.*;
import java.util.concurrent.atomic.*;

/**
 * Streaming Log Analyzer
 * Streaming I/O, parallel computation, latency percentiles (p50, p95, p99)
 */
public class LogAnalyzer {
    private final String name;
    private final AtomicInteger operationCount = new AtomicInteger();

    public LogAnalyzer(String name) {
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
