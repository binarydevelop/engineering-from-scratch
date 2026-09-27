package io.github.javafromscratch.phase66;

/**
 * Phase 66: Optional Done Right
 * Motto: Optional is a return-type signal for absent values, not a field replacement.
 */
public class Phase66Demo {
    private final String topic;

    public Phase66Demo() {
        this.topic = "Optional Done Right";
    }

    public String execute() {
        return "Executed " + topic + ": Optional is a return-type signal for absent values, not a field replacement.";
    }

    public static void main(String[] args) {
        Phase66Demo demo = new Phase66Demo();
        System.out.println(demo.execute());
    }
}
