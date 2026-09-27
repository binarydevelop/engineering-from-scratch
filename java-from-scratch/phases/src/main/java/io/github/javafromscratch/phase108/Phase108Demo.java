package io.github.javafromscratch.phase108;

/**
 * Phase 108: Asynchronous Results: Future
 * Motto: A Future is a handle to a computation that completes in the future.
 */
public class Phase108Demo {
    private final String topic;

    public Phase108Demo() {
        this.topic = "Asynchronous Results: Future";
    }

    public String execute() {
        return "Executed " + topic + ": A Future is a handle to a computation that completes in the future.";
    }

    public static void main(String[] args) {
        Phase108Demo demo = new Phase108Demo();
        System.out.println(demo.execute());
    }
}
