package io.github.javafromscratch.phase16;

/**
 * Phase 16: Constructors & Invariants
 * Motto: An object must never exist in an invalid state; invariants begin in the constructor.
 */
public class Phase16Demo {
    private final String topic;

    public Phase16Demo() {
        this.topic = "Constructors & Invariants";
    }

    public String execute() {
        return "Executed " + topic + ": An object must never exist in an invalid state; invariants begin in the constructor.";
    }

    public static void main(String[] args) {
        Phase16Demo demo = new Phase16Demo();
        System.out.println(demo.execute());
    }
}
