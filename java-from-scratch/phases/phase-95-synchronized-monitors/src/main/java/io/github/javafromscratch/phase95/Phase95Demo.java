package io.github.javafromscratch.phase95;

/**
 * Phase 95: Intrinsic Locks & synchronized
 * Motto: synchronized establishes mutual exclusion and memory visibility across threads.
 */
public class Phase95Demo {
    private final String topic;

    public Phase95Demo() {
        this.topic = "Intrinsic Locks & synchronized";
    }

    public String execute() {
        return "Executed " + topic + ": synchronized establishes mutual exclusion and memory visibility across threads.";
    }

    public static void main(String[] args) {
        Phase95Demo demo = new Phase95Demo();
        System.out.println(demo.execute());
    }
}
