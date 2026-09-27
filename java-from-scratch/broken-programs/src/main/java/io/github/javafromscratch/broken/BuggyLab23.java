package io.github.javafromscratch.broken;

public class BuggyLab23 {
    public int execute(boolean triggerBug) {
        if (triggerBug) {
            throw new RuntimeException("Simulated ClassCastException: Assigning raw type to parameterized variable throws ClassCastException later");
        }
        return 42;
    }
}
