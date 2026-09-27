package io.github.javafromscratch.phase85;

/**
 * Phase 85: Generational Garbage Collection
 * Motto: The Weak Generational Hypothesis: Most allocated objects die young.
 */
public class Phase85Demo {
    private final String topic;

    public Phase85Demo() {
        this.topic = "Generational Garbage Collection";
    }

    public String execute() {
        return "Executed " + topic + ": The Weak Generational Hypothesis: Most allocated objects die young.";
    }

    public static void main(String[] args) {
        Phase85Demo demo = new Phase85Demo();
        System.out.println(demo.execute());
    }
}
