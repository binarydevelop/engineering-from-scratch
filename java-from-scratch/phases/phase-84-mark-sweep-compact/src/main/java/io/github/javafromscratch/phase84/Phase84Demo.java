package io.github.javafromscratch.phase84;

/**
 * Phase 84: Mark, Sweep, and Compact Algorithms
 * Motto: Marking identifies liveness; sweeping reclaims; compacting cures fragmentation.
 */
public class Phase84Demo {
    private final String topic;

    public Phase84Demo() {
        this.topic = "Mark, Sweep, and Compact Algorithms";
    }

    public String execute() {
        return "Executed " + topic + ": Marking identifies liveness; sweeping reclaims; compacting cures fragmentation.";
    }

    public static void main(String[] args) {
        Phase84Demo demo = new Phase84Demo();
        System.out.println(demo.execute());
    }
}
