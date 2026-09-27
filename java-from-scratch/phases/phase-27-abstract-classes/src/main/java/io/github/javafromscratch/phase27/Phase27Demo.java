package io.github.javafromscratch.phase27;

/**
 * Phase 27: Abstract Classes
 * Motto: An abstract class provides partial implementation and enforces template workflows.
 */
public class Phase27Demo {
    private final String topic;

    public Phase27Demo() {
        this.topic = "Abstract Classes";
    }

    public String execute() {
        return "Executed " + topic + ": An abstract class provides partial implementation and enforces template workflows.";
    }

    public static void main(String[] args) {
        Phase27Demo demo = new Phase27Demo();
        System.out.println(demo.execute());
    }
}
