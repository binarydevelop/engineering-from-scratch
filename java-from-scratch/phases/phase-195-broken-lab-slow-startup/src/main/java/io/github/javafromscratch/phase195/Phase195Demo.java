package io.github.javafromscratch.phase195;

/**
 * Phase 195: Broken Lab 09: Slow Startup & Initializer Lockup
 * Motto: Profile blocking work inside static initializers.
 */
public class Phase195Demo {
    private final String topic;

    public Phase195Demo() {
        this.topic = "Broken Lab 09: Slow Startup & Initializer Lockup";
    }

    public String execute() {
        return "Executed " + topic + ": Profile blocking work inside static initializers.";
    }

    public static void main(String[] args) {
        Phase195Demo demo = new Phase195Demo();
        System.out.println(demo.execute());
    }
}
