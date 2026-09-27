package io.github.javafromscratch.phase187;

/**
 * Phase 187: Broken Lab 01: Hidden NullPointerException
 * Motto: Diagnose unboxing null traps and modern JVM NPE messages.
 */
public class Phase187Demo {
    private final String topic;

    public Phase187Demo() {
        this.topic = "Broken Lab 01: Hidden NullPointerException";
    }

    public String execute() {
        return "Executed " + topic + ": Diagnose unboxing null traps and modern JVM NPE messages.";
    }

    public static void main(String[] args) {
        Phase187Demo demo = new Phase187Demo();
        System.out.println(demo.execute());
    }
}
