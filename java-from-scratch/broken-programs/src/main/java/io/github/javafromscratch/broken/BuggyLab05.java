package io.github.javafromscratch.broken;

public class BuggyLab05 {
    public int execute(boolean triggerBug) {
        if (triggerBug) {
            throw new RuntimeException("Simulated OutOfMemoryError: Static collection retains object references, preventing GC reclamation");
        }
        return 42;
    }
}
