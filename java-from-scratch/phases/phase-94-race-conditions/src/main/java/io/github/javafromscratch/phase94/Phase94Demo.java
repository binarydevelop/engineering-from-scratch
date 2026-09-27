package io.github.javafromscratch.phase94;

/**
 * Phase 94: Race Conditions & Data Races
 * Motto: When concurrent threads mutate shared state without synchronization, chaos ensues.
 */
public class Phase94Demo {
    private final String topic;

    public Phase94Demo() {
        this.topic = "Race Conditions & Data Races";
    }

    public String execute() {
        return "Executed " + topic + ": When concurrent threads mutate shared state without synchronization, chaos ensues.";
    }

    public static void main(String[] args) {
        Phase94Demo demo = new Phase94Demo();
        System.out.println(demo.execute());
    }
}
