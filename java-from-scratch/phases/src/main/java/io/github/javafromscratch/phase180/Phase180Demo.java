package io.github.javafromscratch.phase180;

/**
 * Phase 180: Project 10: In-Memory Message Broker
 * Motto: Build an educational pub/sub message broker with bounded queues.
 */
public class Phase180Demo {
    private final String topic;

    public Phase180Demo() {
        this.topic = "Project 10: In-Memory Message Broker";
    }

    public String execute() {
        return "Executed " + topic + ": Build an educational pub/sub message broker with bounded queues.";
    }

    public static void main(String[] args) {
        Phase180Demo demo = new Phase180Demo();
        System.out.println(demo.execute());
    }
}
