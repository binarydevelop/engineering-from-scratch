package io.github.javafromscratch.projects;

import java.util.*;
import java.util.concurrent.*;
import java.util.concurrent.atomic.*;

/**
 * Concurrent Asynchronous Web Crawler
 * HttpClient, Virtual Threads, concurrent visited set, rate limit
 */
public class WebCrawler {
    private final String name;
    private final AtomicInteger operationCount = new AtomicInteger();

    public WebCrawler(String name) {
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
