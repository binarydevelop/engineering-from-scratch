package io.github.javafromscratch.phase200;

/**
 * Phase 200: The Grand Unified Mental Model
 * Motto: Trace a single HTTP request from socket through JVM to database and back.
 */
public class Phase200Demo {
    private final String topic;

    public Phase200Demo() {
        this.topic = "The Grand Unified Mental Model";
    }

    public String execute() {
        return "Executed " + topic + ": Trace a single HTTP request from socket through JVM to database and back.";
    }

    public static void main(String[] args) {
        Phase200Demo demo = new Phase200Demo();
        System.out.println(demo.execute());
    }
}
