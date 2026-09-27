package io.github.javafromscratch.phase154;

/**
 * Phase 154: Rigorous Microbenchmarking with JMH
 * Motto: Never trust a naive timer loop; use JMH to defeat JIT optimizations.
 */
public class Phase154Demo {
    private final String topic;

    public Phase154Demo() {
        this.topic = "Rigorous Microbenchmarking with JMH";
    }

    public String execute() {
        return "Executed " + topic + ": Never trust a naive timer loop; use JMH to defeat JIT optimizations.";
    }

    public static void main(String[] args) {
        Phase154Demo demo = new Phase154Demo();
        System.out.println(demo.execute());
    }
}
