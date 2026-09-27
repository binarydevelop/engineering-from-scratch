package io.github.javafromscratch.broken;

public class BuggyLab03 {
    public int execute(boolean triggerBug) {
        if (triggerBug) {
            throw new RuntimeException("Simulated NoClassDefFoundError: Static initializer throws exception, rendering class permanently uninitializable");
        }
        return 42;
    }
}
