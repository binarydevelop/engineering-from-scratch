package io.github.javafromscratch.phase22;

/**
 * Phase 22: Enums as Finite Sets
 * Motto: An enum is a full Java class with guaranteed singleton instances.
 */
public class Phase22Demo {
    private final String topic;

    public Phase22Demo() {
        this.topic = "Enums as Finite Sets";
    }

    public String execute() {
        return "Executed " + topic + ": An enum is a full Java class with guaranteed singleton instances.";
    }

    public static void main(String[] args) {
        Phase22Demo demo = new Phase22Demo();
        System.out.println(demo.execute());
    }
}
