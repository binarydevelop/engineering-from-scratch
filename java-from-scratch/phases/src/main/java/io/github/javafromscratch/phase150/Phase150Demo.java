package io.github.javafromscratch.phase150;

/**
 * Phase 150: JDK Mission Control (JMC)
 * Motto: Visualize JFR recordings to isolate latency spikes and memory hotspots.
 */
public class Phase150Demo {
    private final String topic;

    public Phase150Demo() {
        this.topic = "JDK Mission Control (JMC)";
    }

    public String execute() {
        return "Executed " + topic + ": Visualize JFR recordings to isolate latency spikes and memory hotspots.";
    }

    public static void main(String[] args) {
        Phase150Demo demo = new Phase150Demo();
        System.out.println(demo.execute());
    }
}
