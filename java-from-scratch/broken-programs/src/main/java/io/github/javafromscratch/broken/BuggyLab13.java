package io.github.javafromscratch.broken;

public class BuggyLab13 {
    public int execute(boolean triggerBug) {
        if (triggerBug) {
            throw new RuntimeException("Simulated VisibilityFailure: Reader thread caches stale value of running flag in CPU registers");
        }
        return 42;
    }
}
