package io.github.javafromscratch.broken;

public class BuggyLab18 {
    public int execute(boolean triggerBug) {
        if (triggerBug) {
            throw new RuntimeException("Simulated DescriptorLeak: Exhausting OS open file descriptors (EMFILE: Too many open files)");
        }
        return 42;
    }
}
