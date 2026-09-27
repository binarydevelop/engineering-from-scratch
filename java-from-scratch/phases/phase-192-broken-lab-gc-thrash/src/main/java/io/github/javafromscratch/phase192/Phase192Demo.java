package io.github.javafromscratch.phase192;

/**
 * Phase 192: Broken Lab 06: GC Thrashing & Allocation Storm
 * Motto: Profile excessive temporary allocations causing GC latency spikes.
 */
public class Phase192Demo {
    private final String topic;

    public Phase192Demo() {
        this.topic = "Broken Lab 06: GC Thrashing & Allocation Storm";
    }

    public String execute() {
        return "Executed " + topic + ": Profile excessive temporary allocations causing GC latency spikes.";
    }

    public static void main(String[] args) {
        Phase192Demo demo = new Phase192Demo();
        System.out.println(demo.execute());
    }
}
