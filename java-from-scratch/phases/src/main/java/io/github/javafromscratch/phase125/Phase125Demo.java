package io.github.javafromscratch.phase125;

/**
 * Phase 125: Database Connection Pooling
 * Motto: Opening a TCP connection to a database per request will crush database performance.
 */
public class Phase125Demo {
    private final String topic;

    public Phase125Demo() {
        this.topic = "Database Connection Pooling";
    }

    public String execute() {
        return "Executed " + topic + ": Opening a TCP connection to a database per request will crush database performance.";
    }

    public static void main(String[] args) {
        Phase125Demo demo = new Phase125Demo();
        System.out.println(demo.execute());
    }
}
