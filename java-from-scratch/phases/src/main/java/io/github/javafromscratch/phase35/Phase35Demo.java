package io.github.javafromscratch.phase35;

/**
 * Phase 35: Autoboxing & Pitfalls
 * Motto: Autoboxing conceals object allocations and injects hidden null hazards.
 */
public class Phase35Demo {
    private final String topic;

    public Phase35Demo() {
        this.topic = "Autoboxing & Pitfalls";
    }

    public String execute() {
        return "Executed " + topic + ": Autoboxing conceals object allocations and injects hidden null hazards.";
    }

    public static void main(String[] args) {
        Phase35Demo demo = new Phase35Demo();
        System.out.println(demo.execute());
    }
}
