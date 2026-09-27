package io.github.javafromscratch.projects;

import java.util.*;
import java.util.concurrent.*;
import java.util.concurrent.atomic.*;

/**
 * Banking Domain & Ledger
 * BigDecimal Money value object, Account invariants, deadlock-free concurrent transfers
 */
public class BankingService {
    private final String name;
    private final AtomicInteger operationCount = new AtomicInteger();

    public BankingService(String name) {
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
