package io.github.javafromscratch.phase86;

/**
 * Phase 86: Modern GC: G1GC vs Generational ZGC
 * Motto: Modern GC trades minor CPU overhead for sub-millisecond pause guarantees.
 */
public class Phase86Demo {
    private final String topic;

    public Phase86Demo() {
        this.topic = "Modern GC: G1GC vs Generational ZGC";
    }

    public String execute() {
        return "Executed " + topic + ": Modern GC trades minor CPU overhead for sub-millisecond pause guarantees.";
    }

    public static void main(String[] args) {
        Phase86Demo demo = new Phase86Demo();
        System.out.println(demo.execute());
    }
}
