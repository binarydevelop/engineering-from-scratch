package io.github.javafromscratch.phase57;

/**
 * Phase 57: Exception Stack Trace Analysis
 * Motto: A stack trace is a photographic snapshot of the call stack at failure time.
 */
public class Phase57Demo {
    private final String topic;

    public Phase57Demo() {
        this.topic = "Exception Stack Trace Analysis";
    }

    public String execute() {
        return "Executed " + topic + ": A stack trace is a photographic snapshot of the call stack at failure time.";
    }

    public static void main(String[] args) {
        Phase57Demo demo = new Phase57Demo();
        System.out.println(demo.execute());
    }
}
