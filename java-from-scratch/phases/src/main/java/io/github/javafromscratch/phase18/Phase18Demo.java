package io.github.javafromscratch.phase18;

/**
 * Phase 18: Encapsulation & Invariants
 * Motto: Exposing internal representation invites external corruption.
 */
public class Phase18Demo {
    private final String topic;

    public Phase18Demo() {
        this.topic = "Encapsulation & Invariants";
    }

    public String execute() {
        return "Executed " + topic + ": Exposing internal representation invites external corruption.";
    }

    public static void main(String[] args) {
        Phase18Demo demo = new Phase18Demo();
        System.out.println(demo.execute());
    }
}
