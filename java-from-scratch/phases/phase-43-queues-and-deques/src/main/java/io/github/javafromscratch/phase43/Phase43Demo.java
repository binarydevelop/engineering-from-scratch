package io.github.javafromscratch.phase43;

/**
 * Phase 43: Queues and Deques
 * Motto: Queues enforce temporal ordering: First-In, First-Out.
 */
public class Phase43Demo {
    private final String topic;

    public Phase43Demo() {
        this.topic = "Queues and Deques";
    }

    public String execute() {
        return "Executed " + topic + ": Queues enforce temporal ordering: First-In, First-Out.";
    }

    public static void main(String[] args) {
        Phase43Demo demo = new Phase43Demo();
        System.out.println(demo.execute());
    }
}
