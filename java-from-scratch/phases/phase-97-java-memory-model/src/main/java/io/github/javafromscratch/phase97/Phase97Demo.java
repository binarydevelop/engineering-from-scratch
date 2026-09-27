package io.github.javafromscratch.phase97;

/**
 * Phase 97: The Java Memory Model (JMM)
 * Motto: The JMM is a contract between the JVM, compiler, hardware, and programmer.
 */
public class Phase97Demo {
    private final String topic;

    public Phase97Demo() {
        this.topic = "The Java Memory Model (JMM)";
    }

    public String execute() {
        return "Executed " + topic + ": The JMM is a contract between the JVM, compiler, hardware, and programmer.";
    }

    public static void main(String[] args) {
        Phase97Demo demo = new Phase97Demo();
        System.out.println(demo.execute());
    }
}
