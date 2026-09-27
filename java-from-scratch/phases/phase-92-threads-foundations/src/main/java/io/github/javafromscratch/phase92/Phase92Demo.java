package io.github.javafromscratch.phase92;

/**
 * Phase 92: Threads from First Principles
 * Motto: A thread is an independent execution context sharing memory with other threads.
 */
public class Phase92Demo {
    private final String topic;

    public Phase92Demo() {
        this.topic = "Threads from First Principles";
    }

    public String execute() {
        return "Executed " + topic + ": A thread is an independent execution context sharing memory with other threads.";
    }

    public static void main(String[] args) {
        Phase92Demo demo = new Phase92Demo();
        System.out.println(demo.execute());
    }
}
