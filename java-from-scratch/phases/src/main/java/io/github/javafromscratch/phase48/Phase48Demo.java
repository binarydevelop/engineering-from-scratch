package io.github.javafromscratch.phase48;

/**
 * Phase 48: Generic Methods
 * Motto: A method can introduce its own type parameters independent of its enclosing class.
 */
public class Phase48Demo {
    private final String topic;

    public Phase48Demo() {
        this.topic = "Generic Methods";
    }

    public String execute() {
        return "Executed " + topic + ": A method can introduce its own type parameters independent of its enclosing class.";
    }

    public static void main(String[] args) {
        Phase48Demo demo = new Phase48Demo();
        System.out.println(demo.execute());
    }
}
