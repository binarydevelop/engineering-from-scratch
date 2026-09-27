package io.github.javafromscratch.broken;

public class BuggyLab32 {
    public int execute(boolean triggerBug) {
        if (triggerBug) {
            throw new RuntimeException("Simulated LazyInitializationException: Accessing uninitialized proxy after persistence session closes");
        }
        return 42;
    }
}
