package io.github.javafromscratch.phase17;

/**
 * Phase 17: The this Reference
 * Motto: this is the hidden zeroth argument passed to every instance method.
 */
public class Phase17Demo {
    private final String topic;

    public Phase17Demo() {
        this.topic = "The this Reference";
    }

    public String execute() {
        return "Executed " + topic + ": this is the hidden zeroth argument passed to every instance method.";
    }

    public static void main(String[] args) {
        Phase17Demo demo = new Phase17Demo();
        System.out.println(demo.execute());
    }
}
