package io.github.javafromscratch.phase116;

/**
 * Phase 116: Virtual Thread Pinning Caveats
 * Motto: synchronized blocks pin virtual threads to carrier threads; use ReentrantLock.
 */
public class Phase116Demo {
    private final String topic;

    public Phase116Demo() {
        this.topic = "Virtual Thread Pinning Caveats";
    }

    public String execute() {
        return "Executed " + topic + ": synchronized blocks pin virtual threads to carrier threads; use ReentrantLock.";
    }

    public static void main(String[] args) {
        Phase116Demo demo = new Phase116Demo();
        System.out.println(demo.execute());
    }
}
