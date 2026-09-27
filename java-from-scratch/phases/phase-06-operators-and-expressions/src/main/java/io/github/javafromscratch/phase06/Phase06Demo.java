package io.github.javafromscratch.phase06;

/**
 * Phase 06: Operators and Expressions
 * Motto: Short-circuit evaluation is both a performance guard and a null defense.
 */
public class Phase06Demo {
    private final String topic;

    public Phase06Demo() {
        this.topic = "Operators and Expressions";
    }

    public String execute() {
        return "Executed " + topic + ": Short-circuit evaluation is both a performance guard and a null defense.";
    }

    public static void main(String[] args) {
        Phase06Demo demo = new Phase06Demo();
        System.out.println(demo.execute());
    }
}
