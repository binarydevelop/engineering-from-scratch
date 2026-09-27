package io.github.javafromscratch.phase55;

/**
 * Phase 55: try, catch, and finally Mechanics
 * Motto: finally blocks execute unconditionally, even in the presence of returns.
 */
public class Phase55Demo {
    private final String topic;

    public Phase55Demo() {
        this.topic = "try, catch, and finally Mechanics";
    }

    public String execute() {
        return "Executed " + topic + ": finally blocks execute unconditionally, even in the presence of returns.";
    }

    public static void main(String[] args) {
        Phase55Demo demo = new Phase55Demo();
        System.out.println(demo.execute());
    }
}
