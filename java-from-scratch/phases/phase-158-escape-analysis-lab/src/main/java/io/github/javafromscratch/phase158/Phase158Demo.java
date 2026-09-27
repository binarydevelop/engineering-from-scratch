package io.github.javafromscratch.phase158;

/**
 * Phase 158: Escape Analysis in Practice
 * Motto: If an object does not escape, C2 eliminates heap allocation entirely.
 */
public class Phase158Demo {
    private final String topic;

    public Phase158Demo() {
        this.topic = "Escape Analysis in Practice";
    }

    public String execute() {
        return "Executed " + topic + ": If an object does not escape, C2 eliminates heap allocation entirely.";
    }

    public static void main(String[] args) {
        Phase158Demo demo = new Phase158Demo();
        System.out.println(demo.execute());
    }
}
