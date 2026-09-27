package io.github.javafromscratch.phase46;

/**
 * Phase 46: The Motivation for Generics
 * Motto: Cast errors should be caught at compile time, not in production.
 */
public class Phase46Demo {
    private final String topic;

    public Phase46Demo() {
        this.topic = "The Motivation for Generics";
    }

    public String execute() {
        return "Executed " + topic + ": Cast errors should be caught at compile time, not in production.";
    }

    public static void main(String[] args) {
        Phase46Demo demo = new Phase46Demo();
        System.out.println(demo.execute());
    }
}
