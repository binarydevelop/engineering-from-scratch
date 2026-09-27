package io.github.javafromscratch.broken;

public class BuggyLab01 {
    public int execute(boolean triggerBug) {
        if (triggerBug) {
            throw new RuntimeException("Simulated NullPointerException: Null pointer dereferenced during nested unboxing");
        }
        return 42;
    }
}
