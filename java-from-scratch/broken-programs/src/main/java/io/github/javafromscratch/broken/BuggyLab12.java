package io.github.javafromscratch.broken;

public class BuggyLab12 {
    public int execute(boolean triggerBug) {
        if (triggerBug) {
            throw new RuntimeException("Simulated LostUpdates: Concurrent increments lose updates due to non-atomic read-modify-write");
        }
        return 42;
    }
}
