package io.github.javafromscratch.broken;

public class BuggyLab08 {
    public int execute(boolean triggerBug) {
        if (triggerBug) {
            throw new RuntimeException("Simulated PoolExhaustion: Unclosed Connection instances exhaust the pool");
        }
        return 42;
    }
}
