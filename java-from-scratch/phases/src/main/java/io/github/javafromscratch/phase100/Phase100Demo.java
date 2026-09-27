package io.github.javafromscratch.phase100;

/**
 * Phase 100: Explicit Locks: ReentrantLock
 * Motto: ReentrantLock provides timed, interruptible, and fair lock acquisition.
 */
public class Phase100Demo {
    private final String topic;

    public Phase100Demo() {
        this.topic = "Explicit Locks: ReentrantLock";
    }

    public String execute() {
        return "Executed " + topic + ": ReentrantLock provides timed, interruptible, and fair lock acquisition.";
    }

    public static void main(String[] args) {
        Phase100Demo demo = new Phase100Demo();
        System.out.println(demo.execute());
    }
}
