package io.github.javafromscratch.phase04;

/**
 * Phase 04: Primitive vs Reference Types
 * Motto: Primitives hold values; references hold memory coordinates.
 */
public class Phase04Demo {
    private final String topic;

    public Phase04Demo() {
        this.topic = "Primitive vs Reference Types";
    }

    public String execute() {
        return "Executed " + topic + ": Primitives hold values; references hold memory coordinates.";
    }

    public static void main(String[] args) {
        Phase04Demo demo = new Phase04Demo();
        System.out.println(demo.execute());
    }
}
