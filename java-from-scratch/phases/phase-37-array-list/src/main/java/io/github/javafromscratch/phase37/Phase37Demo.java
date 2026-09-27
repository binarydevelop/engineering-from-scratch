package io.github.javafromscratch.phase37;

/**
 * Phase 37: ArrayList from Scratch
 * Motto: Contiguous memory guarantees O(1) random access and cache line locality.
 */
public class Phase37Demo {
    private final String topic;

    public Phase37Demo() {
        this.topic = "ArrayList from Scratch";
    }

    public String execute() {
        return "Executed " + topic + ": Contiguous memory guarantees O(1) random access and cache line locality.";
    }

    public static void main(String[] args) {
        Phase37Demo demo = new Phase37Demo();
        System.out.println(demo.execute());
    }
}
