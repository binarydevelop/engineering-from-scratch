package io.github.javafromscratch.broken;

public class BuggyLab02 {
    public int execute(boolean triggerBug) {
        if (triggerBug) {
            throw new RuntimeException("Simulated ConcurrentModificationException: Modifying collection structure while iterating with fail-fast iterator");
        }
        return 42;
    }
}
