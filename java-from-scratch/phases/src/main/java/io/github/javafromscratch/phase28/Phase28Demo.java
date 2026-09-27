package io.github.javafromscratch.phase28;

/**
 * Phase 28: Interfaces as Contracts
 * Motto: Interfaces decouple what a component does from how it is implemented.
 */
public class Phase28Demo {
    private final String topic;

    public Phase28Demo() {
        this.topic = "Interfaces as Contracts";
    }

    public String execute() {
        return "Executed " + topic + ": Interfaces decouple what a component does from how it is implemented.";
    }

    public static void main(String[] args) {
        Phase28Demo demo = new Phase28Demo();
        System.out.println(demo.execute());
    }
}
