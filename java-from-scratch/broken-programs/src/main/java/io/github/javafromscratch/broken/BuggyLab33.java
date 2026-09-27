package io.github.javafromscratch.broken;

public class BuggyLab33 {
    public int execute(boolean triggerBug) {
        if (triggerBug) {
            throw new RuntimeException("Simulated StackOverflowError: Two services require each other in constructor, causing StackOverflowError");
        }
        return 42;
    }
}
