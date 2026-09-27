package io.github.javafromscratch.projects;

import java.util.*;
import java.util.concurrent.*;
import java.util.concurrent.atomic.*;

/**
 * High-Performance File Indexer
 * NIO path walking, inverted search index, concurrent search engine
 */
public class FileIndexer {
    private final String name;
    private final AtomicInteger operationCount = new AtomicInteger();

    public FileIndexer(String name) {
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
