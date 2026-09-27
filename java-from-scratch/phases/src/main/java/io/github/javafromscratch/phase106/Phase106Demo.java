package io.github.javafromscratch.phase106;

/**
 * Phase 106: Thread Pools: ExecutorService
 * Motto: Never spawn raw threads per request; pool and reuse them.
 */
public class Phase106Demo {
    private final String topic;

    public Phase106Demo() {
        this.topic = "Thread Pools: ExecutorService";
    }

    public String execute() {
        return "Executed " + topic + ": Never spawn raw threads per request; pool and reuse them.";
    }

    public static void main(String[] args) {
        Phase106Demo demo = new Phase106Demo();
        System.out.println(demo.execute());
    }
}
