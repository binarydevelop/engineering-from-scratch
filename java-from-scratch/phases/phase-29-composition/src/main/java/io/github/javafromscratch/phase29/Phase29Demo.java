package io.github.javafromscratch.phase29;

/**
 * Phase 29: Composition over Inheritance
 * Motto: Favor 'has-a' over 'is-a' to build flexible, testable architectures.
 */
public class Phase29Demo {
    private final String topic;

    public Phase29Demo() {
        this.topic = "Composition over Inheritance";
    }

    public String execute() {
        return "Executed " + topic + ": Favor 'has-a' over 'is-a' to build flexible, testable architectures.";
    }

    public static void main(String[] args) {
        Phase29Demo demo = new Phase29Demo();
        System.out.println(demo.execute());
    }
}
