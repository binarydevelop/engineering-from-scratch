package io.github.javafromscratch.broken;

public class BuggyLab14 {
    public int execute(boolean triggerBug) {
        if (triggerBug) {
            throw new RuntimeException("Simulated LostUpdates: volatile int count; count++ still suffers from race conditions");
        }
        return 42;
    }
}
