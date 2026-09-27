package io.github.javafromscratch.phase181;

/**
 * Phase 181: Project 11: Mini Dependency Injection Container
 * Motto: Demystify frameworks by building constructor-based dependency injection.
 */
public class Phase181Demo {
    private final String topic;

    public Phase181Demo() {
        this.topic = "Project 11: Mini Dependency Injection Container";
    }

    public String execute() {
        return "Executed " + topic + ": Demystify frameworks by building constructor-based dependency injection.";
    }

    public static void main(String[] args) {
        Phase181Demo demo = new Phase181Demo();
        System.out.println(demo.execute());
    }
}
