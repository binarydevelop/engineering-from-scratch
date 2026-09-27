package io.github.javafromscratch.phase25;

/**
 * Phase 25: Polymorphism & Dispatch
 * Motto: Variables have static compile types; objects have dynamic runtime types.
 */
public class Phase25Demo {
    private final String topic;

    public Phase25Demo() {
        this.topic = "Polymorphism & Dispatch";
    }

    public String execute() {
        return "Executed " + topic + ": Variables have static compile types; objects have dynamic runtime types.";
    }

    public static void main(String[] args) {
        Phase25Demo demo = new Phase25Demo();
        System.out.println(demo.execute());
    }
}
