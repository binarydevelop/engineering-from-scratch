package io.github.javafromscratch.phase13;

/**
 * Phase 13: StringBuilder and Mutation
 * Motto: Repeated string concatenation in loops is an O(N^2) allocation disaster.
 */
public class Phase13Demo {
    private final String topic;

    public Phase13Demo() {
        this.topic = "StringBuilder and Mutation";
    }

    public String execute() {
        return "Executed " + topic + ": Repeated string concatenation in loops is an O(N^2) allocation disaster.";
    }

    public static void main(String[] args) {
        Phase13Demo demo = new Phase13Demo();
        System.out.println(demo.execute());
    }
}
