package io.github.javafromscratch.phase33;

/**
 * Phase 33: Immutable Domain Objects
 * Motto: Immutable objects eliminate shared-mutable-state bugs across threads.
 */
public class Phase33Demo {
    private final String topic;

    public Phase33Demo() {
        this.topic = "Immutable Domain Objects";
    }

    public String execute() {
        return "Executed " + topic + ": Immutable objects eliminate shared-mutable-state bugs across threads.";
    }

    public static void main(String[] args) {
        Phase33Demo demo = new Phase33Demo();
        System.out.println(demo.execute());
    }
}
