package io.github.javafromscratch.phase122;

/**
 * Phase 122: JDBC from First Principles
 * Motto: All Java database persistence reduces to raw JDBC drivers and sockets.
 */
public class Phase122Demo {
    private final String topic;

    public Phase122Demo() {
        this.topic = "JDBC from First Principles";
    }

    public String execute() {
        return "Executed " + topic + ": All Java database persistence reduces to raw JDBC drivers and sockets.";
    }

    public static void main(String[] args) {
        Phase122Demo demo = new Phase122Demo();
        System.out.println(demo.execute());
    }
}
