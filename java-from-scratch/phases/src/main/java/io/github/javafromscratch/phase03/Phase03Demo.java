package io.github.javafromscratch.phase03;

/**
 * Phase 03: Variables and Primitive Types
 * Motto: Memory is a fixed grid of bits; types determine interpretation.
 */
public class Phase03Demo {
    private final String topic;

    public Phase03Demo() {
        this.topic = "Variables and Primitive Types";
    }

    public String execute() {
        return "Executed " + topic + ": Memory is a fixed grid of bits; types determine interpretation.";
    }

    public static void main(String[] args) {
        Phase03Demo demo = new Phase03Demo();
        System.out.println(demo.execute());
    }
}
