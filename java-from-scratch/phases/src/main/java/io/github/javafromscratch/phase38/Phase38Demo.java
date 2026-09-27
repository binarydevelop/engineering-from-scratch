package io.github.javafromscratch.phase38;

/**
 * Phase 38: LinkedList from Scratch
 * Motto: Pointers provide O(1) insertions at known positions but destroy cache locality.
 */
public class Phase38Demo {
    private final String topic;

    public Phase38Demo() {
        this.topic = "LinkedList from Scratch";
    }

    public String execute() {
        return "Executed " + topic + ": Pointers provide O(1) insertions at known positions but destroy cache locality.";
    }

    public static void main(String[] args) {
        Phase38Demo demo = new Phase38Demo();
        System.out.println(demo.execute());
    }
}
