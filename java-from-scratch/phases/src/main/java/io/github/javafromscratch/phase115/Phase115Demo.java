package io.github.javafromscratch.phase115;

/**
 * Phase 115: Platform vs Virtual Threads Benchmark
 * Motto: Virtual threads excel at high-concurrency blocking I/O, not CPU-bound math.
 */
public class Phase115Demo {
    private final String topic;

    public Phase115Demo() {
        this.topic = "Platform vs Virtual Threads Benchmark";
    }

    public String execute() {
        return "Executed " + topic + ": Virtual threads excel at high-concurrency blocking I/O, not CPU-bound math.";
    }

    public static void main(String[] args) {
        Phase115Demo demo = new Phase115Demo();
        System.out.println(demo.execute());
    }
}
