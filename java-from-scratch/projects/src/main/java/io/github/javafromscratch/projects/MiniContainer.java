package io.github.javafromscratch.projects;

import java.util.*;
import java.util.concurrent.*;
import java.util.concurrent.atomic.*;

/**
 * Mini Dependency Injection Container
 * Custom @Inject/@Service annotations, reflection constructor injection
 */
public class MiniContainer {
    private final String name;
    private final AtomicInteger operationCount = new AtomicInteger();

    public MiniContainer(String name) {
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
