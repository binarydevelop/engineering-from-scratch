package io.github.javafromscratch.phase93;

/**
 * Phase 93: Thread Lifecycle & State Transitions
 * Motto: Understand every transition between NEW, RUNNABLE, BLOCKED, and WAITING.
 */
public class Phase93Demo {
    private final String topic;

    public Phase93Demo() {
        this.topic = "Thread Lifecycle & State Transitions";
    }

    public String execute() {
        return "Executed " + topic + ": Understand every transition between NEW, RUNNABLE, BLOCKED, and WAITING.";
    }

    public static void main(String[] args) {
        Phase93Demo demo = new Phase93Demo();
        System.out.println(demo.execute());
    }
}
