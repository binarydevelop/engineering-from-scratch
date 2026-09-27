package io.github.javafromscratch.broken;

public class BuggyLab21 {
    public int execute(boolean triggerBug) {
        if (triggerBug) {
            throw new RuntimeException("Simulated HeapExhaustion: Intermediate stream pipeline without terminal short-circuit exhausts heap");
        }
        return 42;
    }
}
