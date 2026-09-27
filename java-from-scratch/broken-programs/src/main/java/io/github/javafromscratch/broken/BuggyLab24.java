package io.github.javafromscratch.broken;

public class BuggyLab24 {
    public int execute(boolean triggerBug) {
        if (triggerBug) {
            throw new RuntimeException("Simulated ArrayStoreException: Storing incompatible type into Object[] backing Integer[]");
        }
        return 42;
    }
}
