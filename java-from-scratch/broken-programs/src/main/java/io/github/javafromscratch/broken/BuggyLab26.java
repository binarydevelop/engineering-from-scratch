package io.github.javafromscratch.broken;

public class BuggyLab26 {
    public int execute(boolean triggerBug) {
        if (triggerBug) {
            throw new RuntimeException("Simulated LatencyDegradation: Default initial capacity (16) forces continuous array reallocation");
        }
        return 42;
    }
}
