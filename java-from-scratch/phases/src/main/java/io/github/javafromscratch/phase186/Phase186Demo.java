package io.github.javafromscratch.phase186;

/**
 * Phase 186: Project 16: In-Memory Relational Database
 * Motto: Build a relational storage engine with indexing and transaction rollback.
 */
public class Phase186Demo {
    private final String topic;

    public Phase186Demo() {
        this.topic = "Project 16: In-Memory Relational Database";
    }

    public String execute() {
        return "Executed " + topic + ": Build a relational storage engine with indexing and transaction rollback.";
    }

    public static void main(String[] args) {
        Phase186Demo demo = new Phase186Demo();
        System.out.println(demo.execute());
    }
}
