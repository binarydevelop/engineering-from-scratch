package io.github.javafromscratch.phase112;

/**
 * Phase 112: Resource Throttling: Semaphore
 * Motto: A semaphore bounds concurrent access to physical resources.
 */
public class Phase112Demo {
    private final String topic;

    public Phase112Demo() {
        this.topic = "Resource Throttling: Semaphore";
    }

    public String execute() {
        return "Executed " + topic + ": A semaphore bounds concurrent access to physical resources.";
    }

    public static void main(String[] args) {
        Phase112Demo demo = new Phase112Demo();
        System.out.println(demo.execute());
    }
}
