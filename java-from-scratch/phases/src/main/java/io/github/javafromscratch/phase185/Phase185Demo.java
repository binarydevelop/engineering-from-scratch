package io.github.javafromscratch.phase185;

/**
 * Phase 185: Project 15: High-Throughput Log Analyzer
 * Motto: Stream multi-gigabyte log files and compute latency percentiles.
 */
public class Phase185Demo {
    private final String topic;

    public Phase185Demo() {
        this.topic = "Project 15: High-Throughput Log Analyzer";
    }

    public String execute() {
        return "Executed " + topic + ": Stream multi-gigabyte log files and compute latency percentiles.";
    }

    public static void main(String[] args) {
        Phase185Demo demo = new Phase185Demo();
        System.out.println(demo.execute());
    }
}
