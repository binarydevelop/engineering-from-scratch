package io.github.javafromscratch.phase81;

/**
 * Phase 81: The Heap & Compressed OOPs
 * Motto: Heap memory is managed globally; compressed OOPs save 40% memory below 32GB.
 */
public class Phase81Demo {
    private final String topic;

    public Phase81Demo() {
        this.topic = "The Heap & Compressed OOPs";
    }

    public String execute() {
        return "Executed " + topic + ": Heap memory is managed globally; compressed OOPs save 40% memory below 32GB.";
    }

    public static void main(String[] args) {
        Phase81Demo demo = new Phase81Demo();
        System.out.println(demo.execute());
    }
}
