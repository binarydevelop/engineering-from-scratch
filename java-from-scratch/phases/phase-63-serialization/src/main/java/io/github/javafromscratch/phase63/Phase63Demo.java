package io.github.javafromscratch.phase63;

/**
 * Phase 63: Serialization Boundaries & JSON
 * Motto: Java native serialization is a security minefield; prefer explicit text/binary protocols.
 */
public class Phase63Demo {
    private final String topic;

    public Phase63Demo() {
        this.topic = "Serialization Boundaries & JSON";
    }

    public String execute() {
        return "Executed " + topic + ": Java native serialization is a security minefield; prefer explicit text/binary protocols.";
    }

    public static void main(String[] args) {
        Phase63Demo demo = new Phase63Demo();
        System.out.println(demo.execute());
    }
}
