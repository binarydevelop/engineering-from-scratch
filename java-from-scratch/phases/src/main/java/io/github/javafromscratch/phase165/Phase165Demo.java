package io.github.javafromscratch.phase165;

/**
 * Phase 165: Graceful Shutdown Architecture
 * Motto: A production service must finish in-flight requests before exiting on SIGTERM.
 */
public class Phase165Demo {
    private final String topic;

    public Phase165Demo() {
        this.topic = "Graceful Shutdown Architecture";
    }

    public String execute() {
        return "Executed " + topic + ": A production service must finish in-flight requests before exiting on SIGTERM.";
    }

    public static void main(String[] args) {
        Phase165Demo demo = new Phase165Demo();
        System.out.println(demo.execute());
    }
}
