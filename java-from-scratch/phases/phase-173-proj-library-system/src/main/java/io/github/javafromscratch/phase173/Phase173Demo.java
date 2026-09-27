package io.github.javafromscratch.phase173;

/**
 * Phase 173: Project 3: Library Management System
 * Motto: Model domain rules with collections, interfaces, and custom exceptions.
 */
public class Phase173Demo {
    private final String topic;

    public Phase173Demo() {
        this.topic = "Project 3: Library Management System";
    }

    public String execute() {
        return "Executed " + topic + ": Model domain rules with collections, interfaces, and custom exceptions.";
    }

    public static void main(String[] args) {
        Phase173Demo demo = new Phase173Demo();
        System.out.println(demo.execute());
    }
}
