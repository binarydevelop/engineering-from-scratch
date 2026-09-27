package io.github.javafromscratch.projects;

import java.util.*;
import java.util.concurrent.*;
import java.util.concurrent.atomic.*;

/**
 * Mini Test Discovery & Runner
 * Custom @Test/@Before annotations, reflective discovery and execution
 */
public class MiniTestRunner {
    private final String name;
    private final AtomicInteger operationCount = new AtomicInteger();

    public MiniTestRunner(String name) {
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
