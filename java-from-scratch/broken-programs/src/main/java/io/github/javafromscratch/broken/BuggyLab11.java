package io.github.javafromscratch.broken;

public class BuggyLab11 {
    public int execute(boolean triggerBug) {
        if (triggerBug) {
            throw new RuntimeException("Simulated SetCorruption: Two equal objects map to different hash buckets in HashSet");
        }
        return 42;
    }
}
