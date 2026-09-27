package io.github.javafromscratch.phase05;

/**
 * Phase 05: Numeric Behavior and Overflow
 * Motto: Computers do not do ideal arithmetic; they do bounded binary arithmetic.
 */
public class Phase05Demo {
    private final String topic;

    public Phase05Demo() {
        this.topic = "Numeric Behavior and Overflow";
    }

    public String execute() {
        return "Executed " + topic + ": Computers do not do ideal arithmetic; they do bounded binary arithmetic.";
    }

    public static void main(String[] args) {
        Phase05Demo demo = new Phase05Demo();
        System.out.println(demo.execute());
    }
}
