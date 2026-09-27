package io.github.javafromscratch.phase19;

/**
 * Phase 19: Access Modifiers Architecture
 * Motto: Access modifiers define API visibility and module packaging boundaries.
 */
public class Phase19Demo {
    private final String topic;

    public Phase19Demo() {
        this.topic = "Access Modifiers Architecture";
    }

    public String execute() {
        return "Executed " + topic + ": Access modifiers define API visibility and module packaging boundaries.";
    }

    public static void main(String[] args) {
        Phase19Demo demo = new Phase19Demo();
        System.out.println(demo.execute());
    }
}
