package io.github.javafromscratch.phase09;

/**
 * Phase 09: Pass-by-Value Mechanics
 * Motto: Java is strictly pass-by-value: references are passed by value.
 */
public class Phase09Demo {
    private final String topic;

    public Phase09Demo() {
        this.topic = "Pass-by-Value Mechanics";
    }

    public String execute() {
        return "Executed " + topic + ": Java is strictly pass-by-value: references are passed by value.";
    }

    public static void main(String[] args) {
        Phase09Demo demo = new Phase09Demo();
        System.out.println(demo.execute());
    }
}
