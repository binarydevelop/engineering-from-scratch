package io.github.javafromscratch.broken;

public class BuggyLab27 {
    public int execute(boolean triggerBug) {
        if (triggerBug) {
            throw new RuntimeException("Simulated CarrierPinning: Blocking socket call inside synchronized prevents unmounting from carrier");
        }
        return 42;
    }
}
