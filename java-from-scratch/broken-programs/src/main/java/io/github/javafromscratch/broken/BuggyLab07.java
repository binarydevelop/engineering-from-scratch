package io.github.javafromscratch.broken;

public class BuggyLab07 {
    public int execute(boolean triggerBug) {
        if (triggerBug) {
            throw new RuntimeException("Simulated ThreadStarvation: Tasks blocking synchronously on tasks submitted to the same bounded pool");
        }
        return 42;
    }
}
