package io.github.javafromscratch.phase159;

/**
 * Phase 159: The Performance Methodology
 * Motto: Hypothesis-driven tuning: Measure -> Profile -> Hypothesize -> Modify -> Verify.
 */
public class Phase159Demo {
    private final String topic;

    public Phase159Demo() {
        this.topic = "The Performance Methodology";
    }

    public String execute() {
        return "Executed " + topic + ": Hypothesis-driven tuning: Measure -> Profile -> Hypothesize -> Modify -> Verify.";
    }

    public static void main(String[] args) {
        Phase159Demo demo = new Phase159Demo();
        System.out.println(demo.execute());
    }
}
