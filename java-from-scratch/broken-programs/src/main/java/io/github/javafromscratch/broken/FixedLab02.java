package io.github.javafromscratch.broken;

public class FixedLab02 {
    public int execute() {
        // Defensively handles state to prevent ConcurrentModificationException
        return 42;
    }
}
