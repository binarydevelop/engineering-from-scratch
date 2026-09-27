package io.github.javafromscratch.broken;

public class BuggyLab15 {
    public int execute(boolean triggerBug) {
        if (triggerBug) {
            throw new RuntimeException("Simulated LostWakeup: Thread wakes up on spurious wakeup or missed notify");
        }
        return 42;
    }
}
