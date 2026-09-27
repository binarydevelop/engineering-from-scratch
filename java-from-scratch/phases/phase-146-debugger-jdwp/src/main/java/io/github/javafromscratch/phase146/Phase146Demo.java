package io.github.javafromscratch.phase146;

/**
 * Phase 146: Interactive Debugging & JDWP
 * Motto: The debugger connects to the JVM socket to inspect variables and control execution.
 */
public class Phase146Demo {
    private final String topic;

    public Phase146Demo() {
        this.topic = "Interactive Debugging & JDWP";
    }

    public String execute() {
        return "Executed " + topic + ": The debugger connects to the JVM socket to inspect variables and control execution.";
    }

    public static void main(String[] args) {
        Phase146Demo demo = new Phase146Demo();
        System.out.println(demo.execute());
    }
}
