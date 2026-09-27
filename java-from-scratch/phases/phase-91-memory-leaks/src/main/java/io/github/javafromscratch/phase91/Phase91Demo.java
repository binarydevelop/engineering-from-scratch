package io.github.javafromscratch.phase91;

/**
 * Phase 91: Memory Leaks in GC Languages
 * Motto: An object is leaked in Java if it remains reachable but is never used again.
 */
public class Phase91Demo {
    private final String topic;

    public Phase91Demo() {
        this.topic = "Memory Leaks in GC Languages";
    }

    public String execute() {
        return "Executed " + topic + ": An object is leaked in Java if it remains reachable but is never used again.";
    }

    public static void main(String[] args) {
        Phase91Demo demo = new Phase91Demo();
        System.out.println(demo.execute());
    }
}
