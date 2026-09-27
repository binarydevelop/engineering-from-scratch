package io.github.javafromscratch.phase42;

/**
 * Phase 42: TreeMap & TreeSet
 * Motto: Self-balancing binary search trees provide guaranteed O(log N) sorted operations.
 */
public class Phase42Demo {
    private final String topic;

    public Phase42Demo() {
        this.topic = "TreeMap & TreeSet";
    }

    public String execute() {
        return "Executed " + topic + ": Self-balancing binary search trees provide guaranteed O(log N) sorted operations.";
    }

    public static void main(String[] args) {
        Phase42Demo demo = new Phase42Demo();
        System.out.println(demo.execute());
    }
}
