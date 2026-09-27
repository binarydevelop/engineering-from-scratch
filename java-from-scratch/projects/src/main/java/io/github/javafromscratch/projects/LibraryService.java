package io.github.javafromscratch.projects;

import java.util.*;
import java.util.concurrent.*;
import java.util.concurrent.atomic.*;

/**
 * Library Management System
 * Domain state modeling, sequenced collections, custom exceptions, loan tracking
 */
public class LibraryService {
    private final String name;
    private final AtomicInteger operationCount = new AtomicInteger();

    public LibraryService(String name) {
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
