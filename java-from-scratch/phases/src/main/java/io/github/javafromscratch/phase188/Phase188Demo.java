package io.github.javafromscratch.phase188;

/**
 * Phase 188: Broken Lab 02: ConcurrentModificationException
 * Motto: Understand fail-fast collection iterators and modCount.
 */
public class Phase188Demo {
    private final String topic;

    public Phase188Demo() {
        this.topic = "Broken Lab 02: ConcurrentModificationException";
    }

    public String execute() {
        return "Executed " + topic + ": Understand fail-fast collection iterators and modCount.";
    }

    public static void main(String[] args) {
        Phase188Demo demo = new Phase188Demo();
        System.out.println(demo.execute());
    }
}
