package io.github.javafromscratch.phase56;

/**
 * Phase 56: Custom Domain Exceptions
 * Motto: Exceptions should carry structured domain context, not plain error strings.
 */
public class Phase56Demo {
    private final String topic;

    public Phase56Demo() {
        this.topic = "Custom Domain Exceptions";
    }

    public String execute() {
        return "Executed " + topic + ": Exceptions should carry structured domain context, not plain error strings.";
    }

    public static void main(String[] args) {
        Phase56Demo demo = new Phase56Demo();
        System.out.println(demo.execute());
    }
}
