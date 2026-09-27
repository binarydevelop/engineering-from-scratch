package io.github.javafromscratch.phase40;

/**
 * Phase 40: HashMap Correctness & Mutable Keys
 * Motto: Never use a mutable object as a hash map key.
 */
public class Phase40Demo {
    private final String topic;

    public Phase40Demo() {
        this.topic = "HashMap Correctness & Mutable Keys";
    }

    public String execute() {
        return "Executed " + topic + ": Never use a mutable object as a hash map key.";
    }

    public static void main(String[] args) {
        Phase40Demo demo = new Phase40Demo();
        System.out.println(demo.execute());
    }
}
