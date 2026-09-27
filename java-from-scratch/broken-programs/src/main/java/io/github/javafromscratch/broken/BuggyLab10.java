package io.github.javafromscratch.broken;

public class BuggyLab10 {
    public int execute(boolean triggerBug) {
        if (triggerBug) {
            throw new RuntimeException("Simulated KeyLoss: Mutating key field changes hashCode, making entry unfindable");
        }
        return 42;
    }
}
