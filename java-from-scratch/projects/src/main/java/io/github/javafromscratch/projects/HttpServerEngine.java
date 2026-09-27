package io.github.javafromscratch.projects;

import java.util.*;
import java.util.concurrent.*;
import java.util.concurrent.atomic.*;

/**
 * Lightweight HTTP/1.1 Server
 * Raw ServerSocket, HTTP request parser, route dispatch, Virtual Threads
 */
public class HttpServerEngine {
    private final String name;
    private final AtomicInteger operationCount = new AtomicInteger();

    public HttpServerEngine(String name) {
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
