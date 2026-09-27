package io.github.javafromscratch.phase153;

/**
 * Phase 153: Lock Contention & Amdahl's Law
 * Motto: Amdahl's Law: The speedup of a program is limited by its serial fraction.
 */
public class Phase153Demo {
    private final String topic;

    public Phase153Demo() {
        this.topic = "Lock Contention & Amdahl's Law";
    }

    public String execute() {
        return "Executed " + topic + ": Amdahl's Law: The speedup of a program is limited by its serial fraction.";
    }

    public static void main(String[] args) {
        Phase153Demo demo = new Phase153Demo();
        System.out.println(demo.execute());
    }
}
