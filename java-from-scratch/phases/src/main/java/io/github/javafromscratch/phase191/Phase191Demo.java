package io.github.javafromscratch.phase191;

/**
 * Phase 191: Broken Lab 05: Unbounded Static Memory Leak
 * Motto: Find leaked references in static collections via heap dumps.
 */
public class Phase191Demo {
    private final String topic;

    public Phase191Demo() {
        this.topic = "Broken Lab 05: Unbounded Static Memory Leak";
    }

    public String execute() {
        return "Executed " + topic + ": Find leaked references in static collections via heap dumps.";
    }

    public static void main(String[] args) {
        Phase191Demo demo = new Phase191Demo();
        System.out.println(demo.execute());
    }
}
