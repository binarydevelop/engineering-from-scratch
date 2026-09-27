package io.github.javafromscratch.projects;

import java.util.*;
import java.util.concurrent.*;
import java.util.concurrent.atomic.*;

/**
 * In-Memory Message Broker
 * Pub/Sub engine, topics, bounded blocking queues, poison pill shutdown
 */
public class MessageBroker {
    private final String name;
    private final AtomicInteger operationCount = new AtomicInteger();

    public MessageBroker(String name) {
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
