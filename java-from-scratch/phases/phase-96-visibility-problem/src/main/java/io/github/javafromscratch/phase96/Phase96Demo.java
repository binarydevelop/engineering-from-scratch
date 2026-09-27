package io.github.javafromscratch.phase96;

/**
 * Phase 96: Memory Visibility & CPU Caching
 * Motto: Without synchronization, a thread may never observe writes made by another.
 */
public class Phase96Demo {
    private final String topic;

    public Phase96Demo() {
        this.topic = "Memory Visibility & CPU Caching";
    }

    public String execute() {
        return "Executed " + topic + ": Without synchronization, a thread may never observe writes made by another.";
    }

    public static void main(String[] args) {
        Phase96Demo demo = new Phase96Demo();
        System.out.println(demo.execute());
    }
}
