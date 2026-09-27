package io.github.javafromscratch.phase26;

/**
 * Phase 26: Method Overriding vs Overloading
 * Motto: Overloading is resolved statically at compile time; overriding dynamically at runtime.
 */
public class Phase26Demo {
    private final String topic;

    public Phase26Demo() {
        this.topic = "Method Overriding vs Overloading";
    }

    public String execute() {
        return "Executed " + topic + ": Overloading is resolved statically at compile time; overriding dynamically at runtime.";
    }

    public static void main(String[] args) {
        Phase26Demo demo = new Phase26Demo();
        System.out.println(demo.execute());
    }
}
