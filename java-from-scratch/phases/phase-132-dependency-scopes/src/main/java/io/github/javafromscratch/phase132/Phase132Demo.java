package io.github.javafromscratch.phase132;

/**
 * Phase 132: Maven Dependency Scopes
 * Motto: Scopes restrict library visibility across compilation, testing, and runtime.
 */
public class Phase132Demo {
    private final String topic;

    public Phase132Demo() {
        this.topic = "Maven Dependency Scopes";
    }

    public String execute() {
        return "Executed " + topic + ": Scopes restrict library visibility across compilation, testing, and runtime.";
    }

    public static void main(String[] args) {
        Phase132Demo demo = new Phase132Demo();
        System.out.println(demo.execute());
    }
}
