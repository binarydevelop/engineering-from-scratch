package io.github.javafromscratch.phase147;

/**
 * Phase 147: Stack Trace Forensics
 * Motto: Read stack traces backwards from the ultimate root cause.
 */
public class Phase147Demo {
    private final String topic;

    public Phase147Demo() {
        this.topic = "Stack Trace Forensics";
    }

    public String execute() {
        return "Executed " + topic + ": Read stack traces backwards from the ultimate root cause.";
    }

    public static void main(String[] args) {
        Phase147Demo demo = new Phase147Demo();
        System.out.println(demo.execute());
    }
}
