package io.github.javafromscratch.phase70;

/**
 * Phase 70: Streams: Declarative Pipelines
 * Motto: Collections store data in memory; streams compute data through pipelines.
 */
public class Phase70Demo {
    private final String topic;

    public Phase70Demo() {
        this.topic = "Streams: Declarative Pipelines";
    }

    public String execute() {
        return "Executed " + topic + ": Collections store data in memory; streams compute data through pipelines.";
    }

    public static void main(String[] args) {
        Phase70Demo demo = new Phase70Demo();
        System.out.println(demo.execute());
    }
}
