package io.github.javafromscratch.phase189;

/**
 * Phase 189: Broken Lab 03: Classpath Catastrophe
 * Motto: Untangle ClassNotFoundException vs NoClassDefFoundError.
 */
public class Phase189Demo {
    private final String topic;

    public Phase189Demo() {
        this.topic = "Broken Lab 03: Classpath Catastrophe";
    }

    public String execute() {
        return "Executed " + topic + ": Untangle ClassNotFoundException vs NoClassDefFoundError.";
    }

    public static void main(String[] args) {
        Phase189Demo demo = new Phase189Demo();
        System.out.println(demo.execute());
    }
}
