package io.github.javafromscratch.phase14;

/**
 * Phase 14: Classes: State and Behavior
 * Motto: A class defines a type, encapsulation boundaries, and invariant enforcement.
 */
public class Phase14Demo {
    private final String topic;

    public Phase14Demo() {
        this.topic = "Classes: State and Behavior";
    }

    public String execute() {
        return "Executed " + topic + ": A class defines a type, encapsulation boundaries, and invariant enforcement.";
    }

    public static void main(String[] args) {
        Phase14Demo demo = new Phase14Demo();
        System.out.println(demo.execute());
    }
}
