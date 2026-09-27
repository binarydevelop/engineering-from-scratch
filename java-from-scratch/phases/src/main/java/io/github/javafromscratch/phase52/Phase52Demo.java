package io.github.javafromscratch.phase52;

/**
 * Phase 52: Type Erasure & Bytecode Reality
 * Motto: Generics exist purely for the compiler; the JVM bytecode knows almost nothing of them.
 */
public class Phase52Demo {
    private final String topic;

    public Phase52Demo() {
        this.topic = "Type Erasure & Bytecode Reality";
    }

    public String execute() {
        return "Executed " + topic + ": Generics exist purely for the compiler; the JVM bytecode knows almost nothing of them.";
    }

    public static void main(String[] args) {
        Phase52Demo demo = new Phase52Demo();
        System.out.println(demo.execute());
    }
}
