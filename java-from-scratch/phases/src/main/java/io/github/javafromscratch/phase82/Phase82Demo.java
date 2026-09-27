package io.github.javafromscratch.phase82;

/**
 * Phase 82: Escape Analysis & Scalar Replacement
 * Motto: HotSpot does not allocate objects on the stack; it replaces them with scalars.
 */
public class Phase82Demo {
    private final String topic;

    public Phase82Demo() {
        this.topic = "Escape Analysis & Scalar Replacement";
    }

    public String execute() {
        return "Executed " + topic + ": HotSpot does not allocate objects on the stack; it replaces them with scalars.";
    }

    public static void main(String[] args) {
        Phase82Demo demo = new Phase82Demo();
        System.out.println(demo.execute());
    }
}
