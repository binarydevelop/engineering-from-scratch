package io.github.javafromscratch.phase75;

/**
 * Phase 75: Parallel Streams: Pitfalls & Reality
 * Motto: Parallel streams do not automatically make code faster; often they make it slower.
 */
public class Phase75Demo {
    private final String topic;

    public Phase75Demo() {
        this.topic = "Parallel Streams: Pitfalls & Reality";
    }

    public String execute() {
        return "Executed " + topic + ": Parallel streams do not automatically make code faster; often they make it slower.";
    }

    public static void main(String[] args) {
        Phase75Demo demo = new Phase75Demo();
        System.out.println(demo.execute());
    }
}
