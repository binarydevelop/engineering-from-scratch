package io.github.javafromscratch.broken;

public class BuggyLab16 {
    public int execute(boolean triggerBug) {
        if (triggerBug) {
            throw new RuntimeException("Simulated DataPollution: ThreadLocal state bleeds into subsequent tasks executing on the same thread");
        }
        return 42;
    }
}
