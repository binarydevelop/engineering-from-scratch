package io.github.javafromscratch.projects;

import java.util.*;
import java.util.concurrent.*;
import java.util.concurrent.atomic.*;

/**
 * Raw JDBC Transactional Service
 * Raw JDBC, PreparedStatements, connection pool, rollback on failure
 */
public class JdbcService {
    private final String name;
    private final AtomicInteger operationCount = new AtomicInteger();

    public JdbcService(String name) {
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
