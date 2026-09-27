package io.github.javafromscratch.broken;

public class BuggyLab29 {
    public int execute(boolean triggerBug) {
        if (triggerBug) {
            throw new RuntimeException("Simulated SecurityBreach: Malicious SQL injected into dynamic query statement");
        }
        return 42;
    }
}
