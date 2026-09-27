package io.github.javafromscratch.phase174;

/**
 * Phase 174: Project 4: Concurrent Task Runner
 * Motto: Build a resilient concurrent task runner with retries and cancellation.
 */
public class Phase174Demo {
    private final String topic;

    public Phase174Demo() {
        this.topic = "Project 4: Concurrent Task Runner";
    }

    public String execute() {
        return "Executed " + topic + ": Build a resilient concurrent task runner with retries and cancellation.";
    }

    public static void main(String[] args) {
        Phase174Demo demo = new Phase174Demo();
        System.out.println(demo.execute());
    }
}
