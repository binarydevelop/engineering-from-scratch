package io.github.javafromscratch.phase21;

/**
 * Phase 21: Static Members & Class State
 * Motto: Static state is shared across all instances and lives for the classloader lifetime.
 */
public class Phase21Demo {
    private final String topic;

    public Phase21Demo() {
        this.topic = "Static Members & Class State";
    }

    public String execute() {
        return "Executed " + topic + ": Static state is shared across all instances and lives for the classloader lifetime.";
    }

    public static void main(String[] args) {
        Phase21Demo demo = new Phase21Demo();
        System.out.println(demo.execute());
    }
}
