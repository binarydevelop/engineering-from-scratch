package io.github.javafromscratch.phase00;

/**
 * Phase 00: Java Lab & Environment
 * Motto: Before you write code, verify the compiler and runtime.
 */
public class Phase00Demo {
    private final String topic;

    public Phase00Demo() {
        this.topic = "Java Lab & Environment";
    }

    public String execute() {
        return "Executed " + topic + ": Before you write code, verify the compiler and runtime.";
    }

    public static void main(String[] args) {
        Phase00Demo demo = new Phase00Demo();
        System.out.println(demo.execute());
    }
}
