package io.github.javafromscratch.phase103;

/**
 * Phase 103: Low-Level Coordination: wait/notify
 * Motto: Always wait in a loop; never rely on solitary notify.
 */
public class Phase103Demo {
    private final String topic;

    public Phase103Demo() {
        this.topic = "Low-Level Coordination: wait/notify";
    }

    public String execute() {
        return "Executed " + topic + ": Always wait in a loop; never rely on solitary notify.";
    }

    public static void main(String[] args) {
        Phase103Demo demo = new Phase103Demo();
        System.out.println(demo.execute());
    }
}
