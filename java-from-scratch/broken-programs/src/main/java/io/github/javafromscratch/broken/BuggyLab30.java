package io.github.javafromscratch.broken;

public class BuggyLab30 {
    public int execute(boolean triggerBug) {
        if (triggerBug) {
            throw new RuntimeException("Simulated DataInconsistency: First update succeeds but second fails, corrupting ledger balance");
        }
        return 42;
    }
}
