package io.github.javafromscratch.phase162;

/**
 * Phase 162: Startup Latency vs Throughput
 * Motto: CLI tools require fast startup; server backends require high peak throughput.
 */
public class Phase162Demo {
    private final String topic;

    public Phase162Demo() {
        this.topic = "Startup Latency vs Throughput";
    }

    public String execute() {
        return "Executed " + topic + ": CLI tools require fast startup; server backends require high peak throughput.";
    }

    public static void main(String[] args) {
        Phase162Demo demo = new Phase162Demo();
        System.out.println(demo.execute());
    }
}
