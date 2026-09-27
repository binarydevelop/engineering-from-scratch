package io.github.javafromscratch.phase36;

/**
 * Phase 36: Collections Framework Overview
 * Motto: Choose collections by required access semantics, not by habit.
 */
public class Phase36Demo {
    private final String topic;

    public Phase36Demo() {
        this.topic = "Collections Framework Overview";
    }

    public String execute() {
        return "Executed " + topic + ": Choose collections by required access semantics, not by habit.";
    }

    public static void main(String[] args) {
        Phase36Demo demo = new Phase36Demo();
        System.out.println(demo.execute());
    }
}
