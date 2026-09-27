package io.github.javafromscratch.phase44;

/**
 * Phase 44: PriorityQueue from Scratch
 * Motto: A binary heap maintains the extreme element at the root in O(1).
 */
public class Phase44Demo {
    private final String topic;

    public Phase44Demo() {
        this.topic = "PriorityQueue from Scratch";
    }

    public String execute() {
        return "Executed " + topic + ": A binary heap maintains the extreme element at the root in O(1).";
    }

    public static void main(String[] args) {
        Phase44Demo demo = new Phase44Demo();
        System.out.println(demo.execute());
    }
}
