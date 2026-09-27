package io.github.javafromscratch.broken;

public class BuggyLab04 {
    public int execute(boolean triggerBug) {
        if (triggerBug) {
            throw new RuntimeException("Simulated Deadlock: Circular lock acquisition between two threads acquiring locks in reverse order");
        }
        return 42;
    }
}
