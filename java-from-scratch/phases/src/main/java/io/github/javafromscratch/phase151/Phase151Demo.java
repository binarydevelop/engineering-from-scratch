package io.github.javafromscratch.phase151;

/**
 * Phase 151: CPU Profiling: Hot Path Optimization
 * Motto: Optimize the 5% of code where the CPU spends 90% of its cycles.
 */
public class Phase151Demo {
    private final String topic;

    public Phase151Demo() {
        this.topic = "CPU Profiling: Hot Path Optimization";
    }

    public String execute() {
        return "Executed " + topic + ": Optimize the 5% of code where the CPU spends 90% of its cycles.";
    }

    public static void main(String[] args) {
        Phase151Demo demo = new Phase151Demo();
        System.out.println(demo.execute());
    }
}
