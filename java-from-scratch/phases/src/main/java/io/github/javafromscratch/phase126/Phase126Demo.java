package io.github.javafromscratch.phase126;

/**
 * Phase 126: ORM Motivation & Row Mapping
 * Motto: Understand the impedance mismatch between relational tables and object graphs.
 */
public class Phase126Demo {
    private final String topic;

    public Phase126Demo() {
        this.topic = "ORM Motivation & Row Mapping";
    }

    public String execute() {
        return "Executed " + topic + ": Understand the impedance mismatch between relational tables and object graphs.";
    }

    public static void main(String[] args) {
        Phase126Demo demo = new Phase126Demo();
        System.out.println(demo.execute());
    }
}
