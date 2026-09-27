package io.github.javafromscratch.broken;

public class BuggyLab22 {
    public int execute(boolean triggerBug) {
        if (triggerBug) {
            throw new RuntimeException("Simulated CommonPoolStarvation: Parallel stream blocking all worker threads in the JVM common pool");
        }
        return 42;
    }
}
