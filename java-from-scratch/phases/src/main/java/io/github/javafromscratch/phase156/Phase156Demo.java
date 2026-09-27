package io.github.javafromscratch.phase156;

/**
 * Phase 156: Warmup Phenomena & Cold Starts
 * Motto: A freshly started JVM runs in interpreted mode; give it time to optimize.
 */
public class Phase156Demo {
    private final String topic;

    public Phase156Demo() {
        this.topic = "Warmup Phenomena & Cold Starts";
    }

    public String execute() {
        return "Executed " + topic + ": A freshly started JVM runs in interpreted mode; give it time to optimize.";
    }

    public static void main(String[] args) {
        Phase156Demo demo = new Phase156Demo();
        System.out.println(demo.execute());
    }
}
