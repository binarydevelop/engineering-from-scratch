package io.github.javafromscratch.phase15;

/**
 * Phase 15: Objects on the Heap
 * Motto: A class is metadata in Metaspace; an object is live data on the Heap.
 */
public class Phase15Demo {
    private final String topic;

    public Phase15Demo() {
        this.topic = "Objects on the Heap";
    }

    public String execute() {
        return "Executed " + topic + ": A class is metadata in Metaspace; an object is live data on the Heap.";
    }

    public static void main(String[] args) {
        Phase15Demo demo = new Phase15Demo();
        System.out.println(demo.execute());
    }
}
