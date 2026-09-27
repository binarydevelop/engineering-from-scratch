package io.github.javafromscratch.phase136;

/**
 * Phase 136: Dependency Conflicts & Diamond Trees
 * Motto: Two versions of the same library on the classpath lead to runtime version roulette.
 */
public class Phase136Demo {
    private final String topic;

    public Phase136Demo() {
        this.topic = "Dependency Conflicts & Diamond Trees";
    }

    public String execute() {
        return "Executed " + topic + ": Two versions of the same library on the classpath lead to runtime version roulette.";
    }

    public static void main(String[] args) {
        Phase136Demo demo = new Phase136Demo();
        System.out.println(demo.execute());
    }
}
