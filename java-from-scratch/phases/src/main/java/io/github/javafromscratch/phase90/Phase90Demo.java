package io.github.javafromscratch.phase90;

/**
 * Phase 90: Heap Dumps & Object Forensics
 * Motto: A heap dump captures the exact object graph at the moment of failure.
 */
public class Phase90Demo {
    private final String topic;

    public Phase90Demo() {
        this.topic = "Heap Dumps & Object Forensics";
    }

    public String execute() {
        return "Executed " + topic + ": A heap dump captures the exact object graph at the moment of failure.";
    }

    public static void main(String[] args) {
        Phase90Demo demo = new Phase90Demo();
        System.out.println(demo.execute());
    }
}
