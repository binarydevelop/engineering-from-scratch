package io.github.javafromscratch.phase51;

/**
 * Phase 51: The PECS Principle
 * Motto: Use ? extends T when reading data out; use ? super T when putting data in.
 */
public class Phase51Demo {
    private final String topic;

    public Phase51Demo() {
        this.topic = "The PECS Principle";
    }

    public String execute() {
        return "Executed " + topic + ": Use ? extends T when reading data out; use ? super T when putting data in.";
    }

    public static void main(String[] args) {
        Phase51Demo demo = new Phase51Demo();
        System.out.println(demo.execute());
    }
}
