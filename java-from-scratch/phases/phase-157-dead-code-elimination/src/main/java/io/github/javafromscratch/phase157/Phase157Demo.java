package io.github.javafromscratch.phase157;

/**
 * Phase 157: Dead Code & Constant Folding
 * Motto: The C2 compiler ruthlessly deletes code whose results are never observed.
 */
public class Phase157Demo {
    private final String topic;

    public Phase157Demo() {
        this.topic = "Dead Code & Constant Folding";
    }

    public String execute() {
        return "Executed " + topic + ": The C2 compiler ruthlessly deletes code whose results are never observed.";
    }

    public static void main(String[] args) {
        Phase157Demo demo = new Phase157Demo();
        System.out.println(demo.execute());
    }
}
