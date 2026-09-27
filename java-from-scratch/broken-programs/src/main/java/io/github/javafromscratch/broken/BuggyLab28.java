package io.github.javafromscratch.broken;

public class BuggyLab28 {
    public int execute(boolean triggerBug) {
        if (triggerBug) {
            throw new RuntimeException("Simulated SilentFailure: Missing exceptionally() or handle() leaves failure silent");
        }
        return 42;
    }
}
