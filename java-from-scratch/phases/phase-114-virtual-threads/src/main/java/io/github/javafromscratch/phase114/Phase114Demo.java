package io.github.javafromscratch.phase114;

/**
 * Phase 114: Modern Virtual Threads (Project Loom)
 * Motto: Virtual threads make thread-per-request cheap again.
 */
public class Phase114Demo {
    private final String topic;

    public Phase114Demo() {
        this.topic = "Modern Virtual Threads (Project Loom)";
    }

    public String execute() {
        return "Executed " + topic + ": Virtual threads make thread-per-request cheap again.";
    }

    public static void main(String[] args) {
        Phase114Demo demo = new Phase114Demo();
        System.out.println(demo.execute());
    }
}
