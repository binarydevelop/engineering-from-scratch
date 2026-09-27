package io.github.javafromscratch.phase88;

/**
 * Phase 88: Heap Sizing & Container Memory
 * Motto: Setting heap too small causes GC thrashing; setting it too large causes paging.
 */
public class Phase88Demo {
    private final String topic;

    public Phase88Demo() {
        this.topic = "Heap Sizing & Container Memory";
    }

    public String execute() {
        return "Executed " + topic + ": Setting heap too small causes GC thrashing; setting it too large causes paging.";
    }

    public static void main(String[] args) {
        Phase88Demo demo = new Phase88Demo();
        System.out.println(demo.execute());
    }
}
