package io.github.javafromscratch.projects;

import java.util.*;
import java.util.concurrent.*;
import java.util.concurrent.atomic.*;

/**
 * In-Memory Relational Engine
 * Table storage, primary key index, table scan, mini transaction log
 */
public class InMemoryDatabase {
    private final String name;
    private final AtomicInteger operationCount = new AtomicInteger();

    public InMemoryDatabase(String name) {
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
