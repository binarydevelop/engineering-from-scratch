package io.github.javafromscratch.broken;

public class BuggyLab09 {
    public int execute(boolean triggerBug) {
        if (triggerBug) {
            throw new RuntimeException("Simulated ClassInitLockup: Class loading hangs during static initialization");
        }
        return 42;
    }
}
