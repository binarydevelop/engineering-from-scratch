package io.github.javafromscratch.phase183;

/**
 * Phase 183: Project 13: Mini Test Framework
 * Motto: Build a JUnit-like test discovery and execution framework from scratch.
 */
public class Phase183Demo {
    private final String topic;

    public Phase183Demo() {
        this.topic = "Project 13: Mini Test Framework";
    }

    public String execute() {
        return "Executed " + topic + ": Build a JUnit-like test discovery and execution framework from scratch.";
    }

    public static void main(String[] args) {
        Phase183Demo demo = new Phase183Demo();
        System.out.println(demo.execute());
    }
}
