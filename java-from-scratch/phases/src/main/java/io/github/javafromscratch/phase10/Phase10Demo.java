package io.github.javafromscratch.phase10;

/**
 * Phase 10: Arrays from First Principles
 * Motto: An array is a contiguous, fixed-size heap allocation with bounds checks.
 */
public class Phase10Demo {
    private final String topic;

    public Phase10Demo() {
        this.topic = "Arrays from First Principles";
    }

    public String execute() {
        return "Executed " + topic + ": An array is a contiguous, fixed-size heap allocation with bounds checks.";
    }

    public static void main(String[] args) {
        Phase10Demo demo = new Phase10Demo();
        System.out.println(demo.execute());
    }
}
