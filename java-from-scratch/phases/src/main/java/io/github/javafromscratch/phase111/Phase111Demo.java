package io.github.javafromscratch.phase111;

/**
 * Phase 111: Concurrent Collections
 * Motto: Concurrent collections eliminate coarse synchronized bottle-necks.
 */
public class Phase111Demo {
    private final String topic;

    public Phase111Demo() {
        this.topic = "Concurrent Collections";
    }

    public String execute() {
        return "Executed " + topic + ": Concurrent collections eliminate coarse synchronized bottle-necks.";
    }

    public static void main(String[] args) {
        Phase111Demo demo = new Phase111Demo();
        System.out.println(demo.execute());
    }
}
