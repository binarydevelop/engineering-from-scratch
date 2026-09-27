package io.github.javafromscratch.broken;

public class BuggyLab35 {
    public int execute(boolean triggerBug) {
        if (triggerBug) {
            throw new RuntimeException("Simulated StackOverflowError: Method recursive call without base case exhausts 1MB thread stack");
        }
        return 42;
    }
}
