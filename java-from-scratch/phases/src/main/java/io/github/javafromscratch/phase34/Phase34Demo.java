package io.github.javafromscratch.phase34;

/**
 * Phase 34: Primitive Wrapper Types
 * Motto: Wrappers bridge primitives to object-oriented generics at the cost of heap allocation.
 */
public class Phase34Demo {
    private final String topic;

    public Phase34Demo() {
        this.topic = "Primitive Wrapper Types";
    }

    public String execute() {
        return "Executed " + topic + ": Wrappers bridge primitives to object-oriented generics at the cost of heap allocation.";
    }

    public static void main(String[] args) {
        Phase34Demo demo = new Phase34Demo();
        System.out.println(demo.execute());
    }
}
