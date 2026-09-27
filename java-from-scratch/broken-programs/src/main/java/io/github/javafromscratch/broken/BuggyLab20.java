package io.github.javafromscratch.broken;

public class BuggyLab20 {
    public int execute(boolean triggerBug) {
        if (triggerBug) {
            throw new RuntimeException("Simulated PrecisionLoss: 0.1 + 0.2 produces 0.30000000000000004 in account balance");
        }
        return 42;
    }
}
