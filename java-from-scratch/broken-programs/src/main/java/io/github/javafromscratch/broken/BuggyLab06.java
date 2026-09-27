package io.github.javafromscratch.broken;

public class BuggyLab06 {
    public int execute(boolean triggerBug) {
        if (triggerBug) {
            throw new RuntimeException("Simulated ExcessiveGC: Repeated string concatenation in tight loop generates gigabytes of temporary garbage");
        }
        return 42;
    }
}
