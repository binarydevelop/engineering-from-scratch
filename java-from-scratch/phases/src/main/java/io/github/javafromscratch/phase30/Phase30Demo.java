package io.github.javafromscratch.phase30;

/**
 * Phase 30: Object Equality: == vs equals
 * Motto: == tests pointer identity; equals tests semantic value equivalence.
 */
public class Phase30Demo {
    private final String topic;

    public Phase30Demo() {
        this.topic = "Object Equality: == vs equals";
    }

    public String execute() {
        return "Executed " + topic + ": == tests pointer identity; equals tests semantic value equivalence.";
    }

    public static void main(String[] args) {
        Phase30Demo demo = new Phase30Demo();
        System.out.println(demo.execute());
    }
}
