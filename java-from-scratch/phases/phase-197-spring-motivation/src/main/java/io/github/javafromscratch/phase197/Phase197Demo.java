package io.github.javafromscratch.phase197;

/**
 * Phase 197: Deconstructing the Spring Framework
 * Motto: Map framework abstractions to core Java primitives.
 */
public class Phase197Demo {
    private final String topic;

    public Phase197Demo() {
        this.topic = "Deconstructing the Spring Framework";
    }

    public String execute() {
        return "Executed " + topic + ": Map framework abstractions to core Java primitives.";
    }

    public static void main(String[] args) {
        Phase197Demo demo = new Phase197Demo();
        System.out.println(demo.execute());
    }
}
