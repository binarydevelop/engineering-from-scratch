package io.github.javafromscratch.broken;

public class BuggyLab25 {
    public int execute(boolean triggerBug) {
        if (triggerBug) {
            throw new RuntimeException("Simulated NullPointerException: Conditional expression unboxes null wrapper when second branch is primitive");
        }
        return 42;
    }
}
