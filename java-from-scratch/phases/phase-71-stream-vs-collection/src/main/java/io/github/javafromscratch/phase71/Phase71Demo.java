package io.github.javafromscratch.phase71;

/**
 * Phase 71: Stream vs Collection Architecture
 * Motto: A collection is space-bound; a stream is time-bound and single-use.
 */
public class Phase71Demo {
    private final String topic;

    public Phase71Demo() {
        this.topic = "Stream vs Collection Architecture";
    }

    public String execute() {
        return "Executed " + topic + ": A collection is space-bound; a stream is time-bound and single-use.";
    }

    public static void main(String[] args) {
        Phase71Demo demo = new Phase71Demo();
        System.out.println(demo.execute());
    }
}
