package io.github.javafromscratch.phase87;

/**
 * Phase 87: GC Logging and Analysis
 * Motto: If you cannot see your GC pauses, you cannot guarantee your service SLAs.
 */
public class Phase87Demo {
    private final String topic;

    public Phase87Demo() {
        this.topic = "GC Logging and Analysis";
    }

    public String execute() {
        return "Executed " + topic + ": If you cannot see your GC pauses, you cannot guarantee your service SLAs.";
    }

    public static void main(String[] args) {
        Phase87Demo demo = new Phase87Demo();
        System.out.println(demo.execute());
    }
}
