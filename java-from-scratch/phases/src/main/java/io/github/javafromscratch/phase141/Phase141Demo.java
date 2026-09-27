package io.github.javafromscratch.phase141;

/**
 * Phase 141: Integration Testing & Real DBs
 * Motto: Unit tests verify logic; integration tests verify communication with real dependencies.
 */
public class Phase141Demo {
    private final String topic;

    public Phase141Demo() {
        this.topic = "Integration Testing & Real DBs";
    }

    public String execute() {
        return "Executed " + topic + ": Unit tests verify logic; integration tests verify communication with real dependencies.";
    }

    public static void main(String[] args) {
        Phase141Demo demo = new Phase141Demo();
        System.out.println(demo.execute());
    }
}
