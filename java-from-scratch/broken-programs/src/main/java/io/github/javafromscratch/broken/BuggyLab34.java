package io.github.javafromscratch.broken;

public class BuggyLab34 {
    public int execute(boolean triggerBug) {
        if (triggerBug) {
            throw new RuntimeException("Simulated SocketHang: Client blocks on socket read forever when server socket does not close");
        }
        return 42;
    }
}
