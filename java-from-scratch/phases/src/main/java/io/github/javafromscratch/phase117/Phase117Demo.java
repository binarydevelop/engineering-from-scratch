package io.github.javafromscratch.phase117;

/**
 * Phase 117: Concurrency Architecture Comparison
 * Motto: Compare all concurrency models on an identical workload.
 */
public class Phase117Demo {
    private final String topic;

    public Phase117Demo() {
        this.topic = "Concurrency Architecture Comparison";
    }

    public String execute() {
        return "Executed " + topic + ": Compare all concurrency models on an identical workload.";
    }

    public static void main(String[] args) {
        Phase117Demo demo = new Phase117Demo();
        System.out.println(demo.execute());
    }
}
