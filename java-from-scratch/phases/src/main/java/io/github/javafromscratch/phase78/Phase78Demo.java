package io.github.javafromscratch.phase78;

/**
 * Phase 78: Class Loading & Custom Loaders
 * Motto: A class in the JVM is identified by its fully qualified name AND its ClassLoader.
 */
public class Phase78Demo {
    private final String topic;

    public Phase78Demo() {
        this.topic = "Class Loading & Custom Loaders";
    }

    public String execute() {
        return "Executed " + topic + ": A class in the JVM is identified by its fully qualified name AND its ClassLoader.";
    }

    public static void main(String[] args) {
        Phase78Demo demo = new Phase78Demo();
        System.out.println(demo.execute());
    }
}
