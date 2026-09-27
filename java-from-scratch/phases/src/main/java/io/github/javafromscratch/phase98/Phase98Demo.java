package io.github.javafromscratch.phase98;

/**
 * Phase 98: The volatile Modifier
 * Motto: volatile guarantees visibility and ordering, but NOT compound atomicity.
 */
public class Phase98Demo {
    private final String topic;

    public Phase98Demo() {
        this.topic = "The volatile Modifier";
    }

    public String execute() {
        return "Executed " + topic + ": volatile guarantees visibility and ordering, but NOT compound atomicity.";
    }

    public static void main(String[] args) {
        Phase98Demo demo = new Phase98Demo();
        System.out.println(demo.execute());
    }
}
