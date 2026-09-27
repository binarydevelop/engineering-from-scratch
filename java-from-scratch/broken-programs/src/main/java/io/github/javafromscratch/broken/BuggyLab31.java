package io.github.javafromscratch.broken;

public class BuggyLab31 {
    public int execute(boolean triggerBug) {
        if (triggerBug) {
            throw new RuntimeException("Simulated DatabaseOverload: Iterating entities fires separate select query per child record");
        }
        return 42;
    }
}
