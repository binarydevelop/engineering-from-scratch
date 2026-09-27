package io.github.javafromscratch.phase02;

/**
 * Phase 02: The main Method Dissected
 * Motto: Every keyword in the entry point is an architectural contract.
 */
public class Phase02Demo {
    private final String topic;

    public Phase02Demo() {
        this.topic = "The main Method Dissected";
    }

    public String execute() {
        return "Executed " + topic + ": Every keyword in the entry point is an architectural contract.";
    }

    public static void main(String[] args) {
        Phase02Demo demo = new Phase02Demo();
        System.out.println(demo.execute());
    }
}
