package io.github.javafromscratch.phase166;

/**
 * Phase 166: JVM Shutdown Hooks
 * Motto: Shutdown hooks run during JVM termination; keep them fast and non-deadlocking.
 */
public class Phase166Demo {
    private final String topic;

    public Phase166Demo() {
        this.topic = "JVM Shutdown Hooks";
    }

    public String execute() {
        return "Executed " + topic + ": Shutdown hooks run during JVM termination; keep them fast and non-deadlocking.";
    }

    public static void main(String[] args) {
        Phase166Demo demo = new Phase166Demo();
        System.out.println(demo.execute());
    }
}
