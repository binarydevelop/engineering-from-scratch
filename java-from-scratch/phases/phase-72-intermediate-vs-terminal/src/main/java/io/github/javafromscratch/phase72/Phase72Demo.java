package io.github.javafromscratch.phase72;

/**
 * Phase 72: Intermediate vs Terminal Operations
 * Motto: Intermediate stream operations do nothing until a terminal operation demands results.
 */
public class Phase72Demo {
    private final String topic;

    public Phase72Demo() {
        this.topic = "Intermediate vs Terminal Operations";
    }

    public String execute() {
        return "Executed " + topic + ": Intermediate stream operations do nothing until a terminal operation demands results.";
    }

    public static void main(String[] args) {
        Phase72Demo demo = new Phase72Demo();
        System.out.println(demo.execute());
    }
}
