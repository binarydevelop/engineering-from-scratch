package lld.lab;

import java.util.Objects;

/**
 * HelloDomain represents the foundational entity in Phase 00 (LLD Lab).
 * It demonstrates invariant protection, non-blank validation, and behavioral encapsulation.
 */
public class HelloDomain {

    private final String domainName;
    private int operationCount;

    public HelloDomain(String domainName) {
        if (domainName == null || domainName.isBlank()) {
            throw new IllegalArgumentException("Domain name cannot be null or blank");
        }
        this.domainName = domainName.trim();
        this.operationCount = 0;
    }

    public String executeOperation(String command) {
        if (command == null || command.isBlank()) {
            throw new IllegalArgumentException("Command cannot be null or blank");
        }
        this.operationCount++;
        return String.format("[%s] Executed command: %s (total ops: %d)", domainName, command.trim(), operationCount);
    }

    public String getDomainName() {
        return domainName;
    }

    public int getOperationCount() {
        return operationCount;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof HelloDomain that)) return false;
        return Objects.equals(domainName, that.domainName);
    }

    @Override
    public int hashCode() {
        return Objects.hash(domainName);
    }
}
