package io.github.javafromscratch.broken;

public class BuggyLab17 {
    public int execute(boolean triggerBug) {
        if (triggerBug) {
            throw new RuntimeException("Simulated PartiallyInitialized: Publishing this to another thread before constructor finishes establishing invariants");
        }
        return 42;
    }
}
