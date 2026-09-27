package io.github.javafromscratch.projects;

import java.util.*;
import java.util.concurrent.*;
import java.util.concurrent.atomic.*;

/**
 * CLI Application Engine
 * Production CLI with arguments parsing, configuration files, and exit codes
 */
public class CliApp {
    private final String name;
    private final AtomicInteger operationCount = new AtomicInteger();

    public CliApp(String name) {
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
