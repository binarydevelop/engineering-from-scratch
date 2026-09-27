package io.github.javafromscratch.phase127;

/**
 * Phase 127: JPA and Hibernate Basics
 * Motto: An ORM manages entity state transitions and generates SQL on your behalf.
 */
public class Phase127Demo {
    private final String topic;

    public Phase127Demo() {
        this.topic = "JPA and Hibernate Basics";
    }

    public String execute() {
        return "Executed " + topic + ": An ORM manages entity state transitions and generates SQL on your behalf.";
    }

    public static void main(String[] args) {
        Phase127Demo demo = new Phase127Demo();
        System.out.println(demo.execute());
    }
}
