package io.github.javafromscratch.phase128;

/**
 * Phase 128: The N+1 Query Problem
 * Motto: Naively traversing lazy relations executes N+1 database queries; fix with JOIN FETCH.
 */
public class Phase128Demo {
    private final String topic;

    public Phase128Demo() {
        this.topic = "The N+1 Query Problem";
    }

    public String execute() {
        return "Executed " + topic + ": Naively traversing lazy relations executes N+1 database queries; fix with JOIN FETCH.";
    }

    public static void main(String[] args) {
        Phase128Demo demo = new Phase128Demo();
        System.out.println(demo.execute());
    }
}
