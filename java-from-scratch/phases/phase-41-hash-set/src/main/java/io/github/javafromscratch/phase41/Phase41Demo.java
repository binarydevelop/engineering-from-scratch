package io.github.javafromscratch.phase41;

/**
 * Phase 41: HashSet from Scratch
 * Motto: A set is simply a hash map where the values are ignored.
 */
public class Phase41Demo {
    private final String topic;

    public Phase41Demo() {
        this.topic = "HashSet from Scratch";
    }

    public String execute() {
        return "Executed " + topic + ": A set is simply a hash map where the values are ignored.";
    }

    public static void main(String[] args) {
        Phase41Demo demo = new Phase41Demo();
        System.out.println(demo.execute());
    }
}
