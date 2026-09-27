package io.github.javafromscratch.phase53;

/**
 * Phase 53: Exceptions from First Principles
 * Motto: Exceptions provide out-of-band communication of invariant violations.
 */
public class Phase53Demo {
    private final String topic;

    public Phase53Demo() {
        this.topic = "Exceptions from First Principles";
    }

    public String execute() {
        return "Executed " + topic + ": Exceptions provide out-of-band communication of invariant violations.";
    }

    public static void main(String[] args) {
        Phase53Demo demo = new Phase53Demo();
        System.out.println(demo.execute());
    }
}
