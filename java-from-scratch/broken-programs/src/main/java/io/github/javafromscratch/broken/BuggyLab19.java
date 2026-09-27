package io.github.javafromscratch.broken;

public class BuggyLab19 {
    public int execute(boolean triggerBug) {
        if (triggerBug) {
            throw new RuntimeException("Simulated EncodingMismatch: String.getBytes() using default system encoding instead of UTF-8");
        }
        return 42;
    }
}
