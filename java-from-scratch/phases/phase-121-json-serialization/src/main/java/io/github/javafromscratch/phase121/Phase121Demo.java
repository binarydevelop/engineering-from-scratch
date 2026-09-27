package io.github.javafromscratch.phase121;

/**
 * Phase 121: Serialization Boundaries & JSON
 * Motto: Validate and deserialize external untrusted payloads at the network boundary.
 */
public class Phase121Demo {
    private final String topic;

    public Phase121Demo() {
        this.topic = "Serialization Boundaries & JSON";
    }

    public String execute() {
        return "Executed " + topic + ": Validate and deserialize external untrusted payloads at the network boundary.";
    }

    public static void main(String[] args) {
        Phase121Demo demo = new Phase121Demo();
        System.out.println(demo.execute());
    }
}
