package io.github.javafromscratch.phase168;

/**
 * Phase 168: Pluggable Architecture: ServiceLoader
 * Motto: ServiceLoader discovers interface implementations dynamically at runtime.
 */
public class Phase168Demo {
    private final String topic;

    public Phase168Demo() {
        this.topic = "Pluggable Architecture: ServiceLoader";
    }

    public String execute() {
        return "Executed " + topic + ": ServiceLoader discovers interface implementations dynamically at runtime.";
    }

    public static void main(String[] args) {
        Phase168Demo demo = new Phase168Demo();
        System.out.println(demo.execute());
    }
}
