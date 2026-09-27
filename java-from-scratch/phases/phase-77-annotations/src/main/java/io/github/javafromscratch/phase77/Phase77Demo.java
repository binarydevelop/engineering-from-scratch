package io.github.javafromscratch.phase77;

/**
 * Phase 77: Custom Annotations & Processing
 * Motto: Annotations attach metadata to code elements to power framework discovery.
 */
public class Phase77Demo {
    private final String topic;

    public Phase77Demo() {
        this.topic = "Custom Annotations & Processing";
    }

    public String execute() {
        return "Executed " + topic + ": Annotations attach metadata to code elements to power framework discovery.";
    }

    public static void main(String[] args) {
        Phase77Demo demo = new Phase77Demo();
        System.out.println(demo.execute());
    }
}
