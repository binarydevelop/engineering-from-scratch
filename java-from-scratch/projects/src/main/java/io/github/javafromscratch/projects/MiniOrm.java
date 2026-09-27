package io.github.javafromscratch.projects;

import java.util.*;
import java.util.concurrent.*;
import java.util.concurrent.atomic.*;

/**
 * Mini Object-Relational Mapper
 * Custom @Entity/@Id annotations, reflection row mapping, dynamic SQL
 */
public class MiniOrm {
    private final String name;
    private final AtomicInteger operationCount = new AtomicInteger();

    public MiniOrm(String name) {
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
